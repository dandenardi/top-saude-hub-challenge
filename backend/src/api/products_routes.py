from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..infrastructure.db import get_session
from ..schemas.envelope import ApiEnvelope
from ..schemas.common import PaginationIn
from ..schemas.products import ProductIn, ProductOut, ProductUpdate
from ..infrastructure.repos import ProductRepo

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ApiEnvelope[ProductOut], status_code=status.HTTP_201_CREATED)
async def create_product(body: ProductIn, session: AsyncSession = Depends(get_session)):
    existing = await ProductRepo.get_by_sku(session, body.sku)
    if existing:
        return ApiEnvelope.err(mensagem="SKU já cadastrado")
    obj = await ProductRepo.create(session, body)
    return ApiEnvelope.ok(ProductOut.model_validate(obj, from_attributes=True))

@router.get("", response_model=ApiEnvelope[list[ProductOut]])
async def list_products(
    q: str | None = None,
    page: int = 1,
    page_size: int = 20,
    sort: str = "created_at:desc",
    session: AsyncSession = Depends(get_session),
):
    rows, total = await ProductRepo.list(session, q, page, page_size, sort)
    data = [ProductOut.model_validate(r, from_attributes=True) for r in rows]
    
    return ApiEnvelope.ok(data)

@router.get("/{id}", response_model=ApiEnvelope[ProductOut])
async def get_product(id: int, session: AsyncSession = Depends(get_session)):
    obj = await ProductRepo.get_by_id(session, id)
    if not obj:
        return ApiEnvelope.err("Produto não encontrado")
    return ApiEnvelope.ok(ProductOut.model_validate(obj, from_attributes=True))

@router.put("/{id}", response_model=ApiEnvelope[ProductOut])
async def update_product(id: int, body: ProductUpdate, session: AsyncSession = Depends(get_session)):
    obj = await ProductRepo.update(session, id, body)
    if not obj:
        return ApiEnvelope.err("Produto não encontrado")
    return ApiEnvelope.ok(ProductOut.model_validate(obj, from_attributes=True))

@router.delete("/{id}", response_model=ApiEnvelope[None])
async def delete_product(id: int, session: AsyncSession = Depends(get_session)):
    ok = await ProductRepo.delete(session, id)
    if not ok:
        return ApiEnvelope.err("Produto não encontrado")
    return ApiEnvelope.ok(None)
