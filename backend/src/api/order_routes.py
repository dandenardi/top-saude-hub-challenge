from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..infrastructure.db import get_session
from ..application.orders_service import OrdersService
from ..schemas.envelope import ApiEnvelope
from ..schemas.orders import OrderCreateIn, OrderOut  # se não tiver OrderOut, use dict

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=ApiEnvelope[OrderOut])  # ou: ApiEnvelope[dict]
async def create_order(
    body: OrderCreateIn,
    session: AsyncSession = Depends(get_session),
    idempotency_key: str | None = Header(
        default=None, alias="Idempotency-Key", convert_underscores=False
    ),
):
    svc = OrdersService(session)
    env = await svc.create(body, idempotency_key)
    
    return env
