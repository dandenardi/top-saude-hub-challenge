from pydantic import BaseModel, Field
from typing import List

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)

class OrderCreateIn(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    unit_price: int
    quantity: int
    line_total: int

class OrderOut(BaseModel):
    id: int
    customer_id: int
    total_amount: int
    status: str
    items: list[OrderItemOut]

    @classmethod
    def from_orm(cls, o):
        return cls(
            id=o.id,
            customer_id=o.customer_id,
            total_amount=o.total_amount,
            status=o.status,
            items=[OrderItemOut(id=i.id, product_id=i.product_id, unit_price=i.unit_price, quantity=i.quantity, line_total=i.line_total) for i in o.items]
        )
