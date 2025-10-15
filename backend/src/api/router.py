from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from ..infrastructure.db import get_session
from ..schemas.envelope import ApiEnvelope
from ..schemas.products import ProductIn, ProductOut
from ..schemas.customers import CustomerIn, CustomerOut
from ..schemas.orders import OrderCreateIn
from ..application.orders_service import OrdersService
from ..infrastructure.repos import ProductRepo, CustomerRepo

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
async def list_customers(page: int = 1, page_size: int = 20, session: AsyncSession = Depends(get_session)):
    # simplificado: sem filtro/ordem para demo
    from sqlalchemy import select
    rows = (await session.execute(select(__import__("..infrastructure.models", fromlist=["CustomerORM"]).CustomerORM).offset((page-1)*page_size).limit(page_size))).scalars().all()
    return ApiEnvelope.ok([CustomerOut(id=r.id, name=r.name, email=r.email, document=r.document) for r in rows])

# --- Orders ---
@router.post("/orders", response_model=dict)
async def create_order(body: OrderCreateIn, session: AsyncSession = Depends(get_session), idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
    return await OrdersService.create_order(session, body, idempotency_key)
