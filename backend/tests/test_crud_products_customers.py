
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.models import ProductORM, CustomerORM

@pytest.mark.asyncio
async def test_product_crud(session: AsyncSession):
    
    p = ProductORM(name="Prod 1", sku="SKU-1", price=1234, stock_qty=7, is_active=True)
    session.add(p)
    await session.flush()

    
    got = await session.scalar(select(ProductORM).where(ProductORM.id == p.id))
    assert got and got.name == "Prod 1"

    
    got.price = 1500
    await session.flush()
    again = await session.scalar(select(ProductORM).where(ProductORM.id == p.id))
    assert again.price == 1500

    
    await session.delete(again)
    await session.flush()
    gone = await session.scalar(select(ProductORM).where(ProductORM.id == p.id))
    assert gone is None

@pytest.mark.asyncio
async def test_customer_crud(session: AsyncSession):
    c = CustomerORM(name="C1", email="c1@mail.com", document="0001")
    session.add(c)
    await session.flush()

    got = await session.scalar(select(CustomerORM).where(CustomerORM.id == c.id))
    assert got and got.email == "c1@mail.com"

    got.name = "C1-upd"
    await session.flush()
    again = await session.scalar(select(CustomerORM).where(CustomerORM.id == c.id))
    assert again.name == "C1-upd"

    await session.delete(again)
    await session.flush()
    gone = await session.scalar(select(CustomerORM).where(CustomerORM.id == c.id))
    assert gone is None
