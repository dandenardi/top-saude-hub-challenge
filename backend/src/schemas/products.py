from pydantic import BaseModel, Field, constr, conint, ConfigDict
from datetime import datetime
from typing import Optional

SkuStr = constr(strip_whitespace=True, min_length=1, max_length=64)

class ProductIn(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=200)
    sku: SkuStr
    price: conint(ge=0)  
    stock_qty: conint(ge=0)
    is_active: bool = True

class ProductUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=200)] = None
    price: Optional[conint(ge=0)] = None
    stock_qty: Optional[conint(ge=0)] = None
    is_active: Optional[bool] = None

class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    sku: str
    price: int
    stock_qty: int
    is_active: bool
    created_at: datetime
