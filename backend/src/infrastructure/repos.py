from typing import Sequence, Optional, Tuple
from sqlalchemy import select, update, delete, func, asc, desc, text
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ProductORM, CustomerORM

SortableProduct = {
    "id": ProductORM.id,
    "name": ProductORM.name,
    "sku": ProductORM.sku,
    "price": ProductORM.price,
    "stock_qty": ProductORM.stock_qty,
    "created_at": ProductORM.created_at,
}
SortableCustomer = {
    "id": CustomerORM.id,
    "name": CustomerORM.name,
    "email": CustomerORM.email,
    "document": CustomerORM.document,
    "created_at": CustomerORM.created_at,
}

def _parse_sort(sort: str, allowed: dict, tie_id):
    
    try:
        field, direction = sort.split(":")
    except ValueError:
        field, direction = "created_at", "desc"

    col = allowed.get(field, allowed["created_at"])
    is_asc = (direction or "").lower() == "asc"

    primary = asc(col) if is_asc else desc(col)
    tb_asc, tb_desc = tie_id
    secondary = tb_asc if is_asc else tb_desc
    return primary, secondary

class ProductRepo:
    @staticmethod
    async def create(session: AsyncSession, data) -> ProductORM:
        obj = ProductORM(**data.model_dump())
        session.add(obj)
        await session.flush()
        await session.refresh(obj)
        return obj

    @staticmethod
    async def get_by_id(session: AsyncSession, id: int) -> Optional[ProductORM]:
        res = await session.execute(select(ProductORM).where(ProductORM.id == id))
        return res.scalar_one_or_none()

    @staticmethod
    async def get_by_sku(session: AsyncSession, sku: str) -> Optional[ProductORM]:
        res = await session.execute(select(ProductORM).where(ProductORM.sku == sku))
        return res.scalar_one_or_none()

    @staticmethod
    async def update(session: AsyncSession, id: int, data) -> Optional[ProductORM]:
        values = {k: v for k, v in data.model_dump(exclude_unset=True).items()}
        if not values:
            return await ProductRepo.get_by_id(session, id)
        await session.execute(
            update(ProductORM).where(ProductORM.id == id).values(**values)
        )
        await session.flush()
        return await ProductRepo.get_by_id(session, id)

    @staticmethod
    async def delete(session: AsyncSession, id: int) -> bool:
        res = await session.execute(delete(ProductORM).where(ProductORM.id == id))
        return res.rowcount > 0

    @staticmethod
    async def list(
        session: AsyncSession,
        q: Optional[str],
        page: int,
        page_size: int,
        sort: str,
    ) -> Tuple[Sequence[ProductORM], int]:
        stmt = select(ProductORM)
        if q:
            like = f"%{q}%"
            stmt = stmt.where(
                (ProductORM.name.ilike(like)) | (ProductORM.sku.ilike(like))
            )
        total = await session.scalar(select(func.count()).select_from(stmt.subquery()))
        primary, secondary = _parse_sort(sort, SortableProduct, (ProductORM.id.asc(), ProductORM.id.desc()),)
        stmt = stmt.order_by(primary, secondary)
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        rows = (await session.execute(stmt)).scalars().all()
        return rows, int(total or 0)

class CustomerRepo:
    @staticmethod
    async def create(session: AsyncSession, data) -> CustomerORM:
        obj = CustomerORM(**data.model_dump())
        session.add(obj)
        await session.flush()
        await session.refresh(obj)
        return obj

    @staticmethod
    async def get_by_id(session: AsyncSession, id: int) -> Optional[CustomerORM]:
        res = await session.execute(select(CustomerORM).where(CustomerORM.id == id))
        return res.scalar_one_or_none()

    @staticmethod
    async def get_by_document(session: AsyncSession, document: str) -> Optional[CustomerORM]:
        res = await session.execute(select(CustomerORM).where(CustomerORM.document == document))
        return res.scalar_one_or_none()

    @staticmethod
    async def update(session: AsyncSession, id: int, data) -> Optional[CustomerORM]:
        values = {k: v for k, v in data.model_dump(exclude_unset=True).items()}
        if not values:
            return await CustomerRepo.get_by_id(session, id)
        await session.execute(
            update(CustomerORM).where(CustomerORM.id == id).values(**values)
        )
        await session.flush()
        return await CustomerRepo.get_by_id(session, id)

    @staticmethod
    async def delete(session: AsyncSession, id: int) -> bool:
        res = await session.execute(delete(CustomerORM).where(CustomerORM.id == id))
        return res.rowcount > 0

    @staticmethod
    async def list(
        session: AsyncSession,
        q: Optional[str],
        page: int,
        page_size: int,
        sort: str,
    ) -> Tuple[Sequence[CustomerORM], int]:
        stmt = select(CustomerORM)
        if q:
            like = f"%{q}%"
            stmt = stmt.where(
                (CustomerORM.name.ilike(like))
                | (CustomerORM.email.ilike(like))
                | (CustomerORM.document.ilike(like))
            )
        total = await session.scalar(select(func.count()).select_from(stmt.subquery()))
        primary, secondary = _parse_sort(sort, SortableCustomer, (CustomerORM.id.asc(), CustomerORM.id.desc()),)
        stmt = stmt.order_by(primary, secondary)
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        rows = (await session.execute(stmt)).scalars().all()
        return rows, int(total or 0)
