from pydantic import BaseModel, Field

class ProductIn(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    sku: str
    price: int = Field(ge=0)
    stock_qty: int = Field(ge=0)
    is_active: bool = True

class ProductOut(ProductIn):
    id: int
