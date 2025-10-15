from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from ..infrastructure.models import ProductORM, OrderORM, OrderItemORM, IdempotencyKeyORM
from ..domain.enums import OrderStatus
from ..schemas.orders import OrderCreateIn, OrderOut
from ..schemas.envelope import ApiEnvelope
import json

class OrdersService:
    @staticmethod
    async def create_order(session: AsyncSession, payload: OrderCreateIn, idempotency_key: str | None):
        # Idempotência
        if idempotency_key:
            existing = (await session.execute(select(IdempotencyKeyORM).where(IdempotencyKeyORM.key == idempotency_key))).scalar_one_or_none()
            if existing and existing.response_json:
                return json.loads(existing.response_json)

        # Transação atômica
        async with session.begin():
            product_ids = [item.product_id for item in payload.items]
            products = (await session.execute(
                select(ProductORM).where(ProductORM.id.in_(product_ids)).with_for_update()
            )).scalars().all()

            prod_by_id = {p.id: p for p in products}
            total = 0
            for item in payload.items:
                p = prod_by_id.get(item.product_id)
                if not p or not p.is_active:
                    raise ValueError("Produto inválido ou inativo")
                if p.stock_qty < item.quantity:
                    raise ValueError("Estoque insuficiente")
                total += p.price * item.quantity

            order = OrderORM(customer_id=payload.customer_id, total_amount=total, status=OrderStatus.CREATED)
            session.add(order)
            await session.flush()  # garante order.id

            for item in payload.items:
                p = prod_by_id[item.product_id]
                p.stock_qty -= item.quantity
                session.add(OrderItemORM(
                    order_id=order.id,
                    product_id=p.id,
                    unit_price=p.price,
                    quantity=item.quantity,
                    line_total=p.price * item.quantity,
                ))

        order_db = (await session.execute(
            select(OrderORM).options(selectinload(OrderORM.items)).where(OrderORM.id == order.id)
        )).scalar_one()

        result = ApiEnvelope.ok(OrderOut.from_orm(order_db).model_dump()).model_dump()

        if idempotency_key:
            record = IdempotencyKeyORM(key=idempotency_key, order_id=order_db.id, response_json=json.dumps(result))
            session.add(record)
            await session.commit()

        return result
