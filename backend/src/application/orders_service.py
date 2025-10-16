import json
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from ..infrastructure.models import ProductORM, OrderORM, OrderItemORM, IdempotencyKeyORM
from ..schemas.envelope import ApiEnvelope
from ..schemas.orders import OrderCreateIn, OrderOut
import structlog

log = structlog.get_logger()

class OrdersService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: OrderCreateIn, idem_key: str | None):
        if not payload.items:
            return ApiEnvelope.err("Pedido sem itens")

        if idem_key:
            
            found = (
                await self.session.execute(
                    select(IdempotencyKeyORM).where(IdempotencyKeyORM.key == idem_key)
                )
            ).scalar_one_or_none()
            if found and found.response_json:
                data = json.loads(found.response_json)
                out = OrderOut.model_validate(data)
                log.info("idempotent_replay", key=idem_key)
                return ApiEnvelope.ok(out)

        async def _inside_tx():
            ids = [i.product_id for i in payload.items]
            prods = (
                await self.session.execute(
                    select(ProductORM)
                    .where(ProductORM.id.in_(ids))
                    .with_for_update()
                )
            ).scalars().all()
            pmap = {p.id: p for p in prods}

            
            for it in payload.items:
                p = pmap.get(it.product_id)
                if not p or not p.is_active:
                    log.warning("order_create_validation_error", reason="inactive_or_missing", product_id=it.product_id)
                    return ApiEnvelope.err("Produto inválido ou inativo")
                if p.stock_qty < it.quantity:
                    log.warning("order_create_validation_error", reason="lack_of_stock_for_product", product_id=it.product_id)
                    return ApiEnvelope.err(f"Estoque insuficiente para produto {p.name}")

            order = OrderORM(customer_id=payload.customer_id, status="CREATED", total_amount=0)
            self.session.add(order)
            await self.session.flush()  

            total = 0
            for it in payload.items:
                p = pmap[it.product_id]
                line_total = p.price * it.quantity
                total += line_total
                self.session.add(
                    OrderItemORM(
                        order_id=order.id,
                        product_id=p.id,
                        unit_price=p.price,
                        quantity=it.quantity,
                        line_total=line_total,
                    )
                )
                p.stock_qty -= it.quantity

            order.total_amount = total
            await self.session.flush()

            
            rec = await self.session.execute(
                select(OrderORM)
                .options(selectinload(OrderORM.items))
                .where(OrderORM.id == order.id)
            )
            order_loaded = rec.scalar_one()
            

            
            out = OrderOut.from_orm(order_loaded)  
            out_json = json.dumps(out.model_dump(), ensure_ascii=False)

            
            if idem_key:
                stmt = insert(IdempotencyKeyORM).values(
                    key=idem_key,
                    order_id=order_loaded.id,
                    response_json=out_json,
                ).on_conflict_do_nothing(
                    index_elements=[IdempotencyKeyORM.key]
                )
                await self.session.execute(stmt)
            log.info("order_created", order_id=order_loaded.id, customer_id=payload.customer_id, total=order_loaded.total_amount)
            return ApiEnvelope.ok(out)
    
        try:

            if self.session.in_transaction():
                async with self.session.begin_nested():
                    return await _inside_tx()
            else:
                async with self.session.begin():
                    return await _inside_tx()
        except Exception as e:
            
            return ApiEnvelope.err(str(e))