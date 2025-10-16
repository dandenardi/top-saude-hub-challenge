# backend/src/infrastructure/repos.py
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from .models import ProductORM, CustomerORM
from ..schemas.products import ProductIn, ProductOut
from ..schemas.customers import CustomerIn, CustomerOut

class ProductRepo:
    @staticmethod
    async def create(session: AsyncSession, body: ProductIn) -> ProductOut:
        db = ProductORM(**body.model_dump())
        session.add(db)
        await session.flush()          
        
        return ProductOut(
            id=db.id,
            name=db.name,
            sku=db.sku,
            price=db.price,
            stock_qty=db.stock_qty,
            is_active=db.is_active,
        )

    @staticmethod
    async def list(session: AsyncSession, q: str | None, page: int, page_size: int, sort: str):
        sort_col, sort_dir = (sort.split(":", 1) + ["asc"])[:2]
        order_expr = text(f"{sort_col} {sort_dir.upper()}")
        stmt = select(ProductORM).order_by(order_expr)
        if q:
            stmt = stmt.where(ProductORM.name.ilike(f"%{q}%"))
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        rows = (await session.execute(stmt)).scalars().all()
        return [
            ProductOut(
                id=r.id, name=r.name, sku=r.sku, price=r.price,
                stock_qty=r.stock_qty, is_active=r.is_active
            )
            for r in rows
        ]

class CustomerRepo:
    @staticmethod
    async def create(session: AsyncSession, body: CustomerIn) -> CustomerOut:
        db = CustomerORM(**body.model_dump())
        session.add(db)
        await session.flush()          
        return CustomerOut(id=db.id, name=db.name, email=db.email, document=db.document)
