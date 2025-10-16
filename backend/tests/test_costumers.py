import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.models import CustomerORM

@pytest.mark.asyncio
async def test_customer_crud_unit(session: AsyncSession):
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
