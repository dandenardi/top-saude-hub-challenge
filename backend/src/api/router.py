from fastapi import APIRouter
from .products_routes import router as products_router
from .customers_routes import router as customers_router
from .order_routes import router as orders_router 

router = APIRouter()
router.include_router(products_router)
router.include_router(customers_router)
router.include_router(orders_router)
