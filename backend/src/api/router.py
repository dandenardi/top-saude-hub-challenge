from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from ..infrastructure.db import get_session
from ..schemas.envelope import ApiEnvelope
from ..schemas.products import ProductIn, ProductOut
from ..schemas.customers import CustomerIn, CustomerOut
from ..schemas.orders import OrderCreateIn
from ..application.orders_service import OrdersService
from ..infrastructure.repos import ProductRepo, CustomerRepo
from ..infrastructure.models import CustomerORM

router = APIRouter()

# --- Products CRUD ---
@router.post("/products", response_model=ApiEnvelope[ProductOut])
async def create_product(body: ProductIn, session: AsyncSession = Depends(get_session)):
    out = await ProductRepo.create(session, body)
    return ApiEnvelope.ok(out)

@router.get("/products", response_model=ApiEnvelope[list[ProductOut]])
async def list_products(q: str | None = None, page: int = 1, page_size: int = 20, sort: str = "created_at:desc", session: AsyncSession = Depends(get_session)):
    data = await ProductRepo.list(session, q=q, page=page, page_size=page_size, sort=sort)
    return ApiEnvelope.ok(data)

# --- Customers CRUD ---
@router.post("/customers", response_model=ApiEnvelope[CustomerOut])
async def create_customer(body: CustomerIn, session: AsyncSession = Depends(get_session)):
    out = await CustomerRepo.create(session, body)
    return ApiEnvelope.ok(out)

@router.get("/customers", response_model=ApiEnvelope[list[CustomerOut]])
async def list_customers(
    q: str | None = None,
    page: int = 1,
    page_size: int = 20,
    sort: str = "created_at:desc",
    session: AsyncSession = Depends(get_session),
):
    sort_col, sort_dir = (sort.split(":", 1) + ["asc"])[:2]
    order_expr = text(f"{sort_col} {sort_dir.upper()}")
    stmt = select(CustomerORM).order_by(order_expr)
    if q:
        stmt = stmt.where(CustomerORM.name.ilike(f"%{q}%"))
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    rows = (await session.execute(stmt)).scalars().all()
    data = [CustomerOut(id=r.id, name=r.name, email=r.email, document=r.document) for r in rows]
    return ApiEnvelope.ok(data)

# --- Orders ---
@router.post("/orders", response_model=dict)
async def create_order(
    body: OrderCreateIn,
    session: AsyncSession = Depends(get_session),
    
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key", convert_underscores=False),
):
    svc = OrdersService(session)
    env = await svc.create(body, idempotency_key)

    return JSONResponse(
        status_code=getattr(env, "status_code", status.HTTP_200_OK),
        content=env.model_dump(),
    )
    
  
