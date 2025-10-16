from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..infrastructure.db import get_session
from ..schemas.envelope import ApiEnvelope
from ..schemas.customers import CustomerIn, CustomerOut, CustomerUpdate
from ..infrastructure.repos import CustomerRepo

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("", response_model=ApiEnvelope[CustomerOut])
async def create_customer(body: CustomerIn, session: AsyncSession = Depends(get_session)):
    exists = await CustomerRepo.get_by_document(session, body.document)
    if exists:
        return ApiEnvelope.err("Documento já cadastrado")
    obj = await CustomerRepo.create(session, body)
    return ApiEnvelope.ok(CustomerOut.model_validate(obj))

@router.get("", response_model=ApiEnvelope[list[CustomerOut]])
async def list_customers(
    q: str | None = None,
    page: int = 1,
    page_size: int = 20,
    sort: str = "created_at:desc",
    session: AsyncSession = Depends(get_session),
):
    rows, total = await CustomerRepo.list(session, q, page, page_size, sort)
    data = [CustomerOut.model_validate(r) for r in rows]
    return ApiEnvelope.ok(data)

@router.get("/{id}", response_model=ApiEnvelope[CustomerOut])
async def get_customer(id: int, session: AsyncSession = Depends(get_session)):
    obj = await CustomerRepo.get_by_id(session, id)
    if not obj:
        return ApiEnvelope.err("Cliente não encontrado")
    return ApiEnvelope.ok(CustomerOut.model_validate(obj))

@router.put("/{id}", response_model=ApiEnvelope[CustomerOut])
async def update_customer(id: int, body: CustomerUpdate, session: AsyncSession = Depends(get_session)):
    obj = await CustomerRepo.update(session, id, body)
    if not obj:
        return ApiEnvelope.err("Cliente não encontrado")
    return ApiEnvelope.ok(CustomerOut.model_validate(obj))

@router.delete("/{id}", response_model=ApiEnvelope[None])
async def delete_customer(id: int, session: AsyncSession = Depends(get_session)):
    ok = await CustomerRepo.delete(session, id)
    if not ok:
        return ApiEnvelope.err("Cliente não encontrado")
    return ApiEnvelope.ok(None)
