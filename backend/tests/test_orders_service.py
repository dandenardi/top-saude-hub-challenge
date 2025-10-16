
import json
import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.application.orders_service import OrdersService
from src.infrastructure.models import ProductORM, OrderORM, OrderItemORM, IdempotencyKeyORM
from src.schemas.orders import OrderCreateIn

@pytest.mark.asyncio
async def test_create_order_success_decrements_stock_and_persists_items(session: AsyncSession, mk_product, mk_customer):
    p1 = await mk_product(price=3990, stock_qty=20)
    p2 = await mk_product(price=1390, stock_qty=10)
    c  = await mk_customer()

    payload = OrderCreateIn(customer_id=c.id, items=[
        {"product_id": p1.id, "quantity": 3},
        {"product_id": p2.id, "quantity": 2},
    ])

    svc = OrdersService(session)
    env = await svc.create(payload, idem_key=None)

    assert env.cod_retorno == 0
    assert env.data is not None
    assert env.data.total_amount == 3*3990 + 2*1390
    assert len(env.data.items) == 2

    
    p1_db = await session.scalar(select(ProductORM).where(ProductORM.id == p1.id))
    p2_db = await session.scalar(select(ProductORM).where(ProductORM.id == p2.id))
    assert p1_db.stock_qty == 17
    assert p2_db.stock_qty == 8

    
    order_db = await session.scalar(
        select(OrderORM).where(OrderORM.id == env.data.id)
    )
    assert order_db is not None

    items = (await session.execute(
        select(OrderItemORM).where(OrderItemORM.order_id == order_db.id)
    )).scalars().all()
    assert {i.product_id for i in items} == {p1.id, p2.id}

@pytest.mark.asyncio
async def test_create_order_error_when_empty_items(session: AsyncSession, mk_customer):
    c = await mk_customer()
    payload = OrderCreateIn(customer_id=c.id, items=[])
    svc = OrdersService(session)
    env = await svc.create(payload, idem_key=None)

    assert env.cod_retorno == 1
    assert "Pedido sem itens" in (env.mensagem or "")

@pytest.mark.asyncio
async def test_create_order_error_when_product_inactive(session: AsyncSession, mk_product, mk_customer):
    inactive = await mk_product(is_active=False)
    c = await mk_customer()
    payload = OrderCreateIn(customer_id=c.id, items=[{"product_id": inactive.id, "quantity": 1}])

    svc = OrdersService(session)
    env = await svc.create(payload, idem_key=None)

    assert env.cod_retorno == 1
    assert "inativo" in (env.mensagem or "").lower()

@pytest.mark.asyncio
async def test_create_order_error_when_insufficient_stock(session: AsyncSession, mk_product, mk_customer):
    p = await mk_product(stock_qty=2)
    c = await mk_customer()
    payload = OrderCreateIn(customer_id=c.id, items=[{"product_id": p.id, "quantity": 5}])

    svc = OrdersService(session)
    env = await svc.create(payload, idem_key=None)

    assert env.cod_retorno == 1
    assert "estoque" in (env.mensagem or "").lower()

@pytest.mark.asyncio
async def test_idempotency_replay_returns_same_payload_and_no_double_effect(session: AsyncSession, mk_product, mk_customer):
    p = await mk_product(price=1000, stock_qty=10)
    c = await mk_customer()
    payload = OrderCreateIn(customer_id=c.id, items=[{"product_id": p.id, "quantity": 2}])

    svc = OrdersService(session)

    
    env1 = await svc.create(payload, idem_key="abc-123")
    assert env1.cod_retorno == 0
    order_id_1 = env1.data.id

   
    p_after_1 = await session.scalar(select(ProductORM).where(ProductORM.id == p.id))
    assert p_after_1.stock_qty == 8

   
    env2 = await svc.create(payload, idem_key="abc-123")
    assert env2.cod_retorno == 0
    
    assert env2.data.id == order_id_1

    
    p_after_2 = await session.scalar(select(ProductORM).where(ProductORM.id == p.id))
    assert p_after_2.stock_qty == 8

    
    idem = await session.scalar(select(IdempotencyKeyORM).where(IdempotencyKeyORM.key == "abc-123"))
    assert idem is not None and idem.response_json
    parsed = json.loads(idem.response_json)
    assert parsed["id"] == order_id_1

@pytest.mark.asyncio
async def test_atomicity_rollback_on_mid_failure(engine, session, mk_product, mk_customer, monkeypatch):
    
    p1 = await mk_product(stock_qty=5, price=100)
    p2 = await mk_product(stock_qty=5, price=100)
    c  = await mk_customer()

    
    await session.commit()

    
    factory = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    async with factory() as s_op:
        svc = OrdersService(s_op)

        original_flush = s_op.flush
        call_count = {"n": 0}

        async def bomb_flush(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 2:
                raise RuntimeError("boom")
            return await original_flush(*args, **kwargs)

        monkeypatch.setattr(s_op, "flush", bomb_flush)

        payload = OrderCreateIn(
            customer_id=c.id,
            items=[
                {"product_id": p1.id, "quantity": 3},
                {"product_id": p2.id, "quantity": 3},
            ],
        )

        env = await svc.create(payload, idem_key=None)
        assert env.cod_retorno == 1  # erro envelopado

    
    async with factory() as s_check:
        p1_db = await s_check.scalar(select(ProductORM).where(ProductORM.id == p1.id))
        p2_db = await s_check.scalar(select(ProductORM).where(ProductORM.id == p2.id))
        assert p1_db is not None and p1_db.stock_qty == 5
        assert p2_db is not None and p2_db.stock_qty == 5