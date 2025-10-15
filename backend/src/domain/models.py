from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from .enums import OrderStatus

@dataclass(slots=True)
class Product:
    id: int
    name: str
    sku: str
    price: int  # cents
    stock_qty: int
    is_active: bool
    created_at: datetime

@dataclass(slots=True)
class Customer:
    id: int
    name: str
    email: str
    document: str
    created_at: datetime

@dataclass(slots=True)
class OrderItem:
    id: int
    product_id: int
    unit_price: int
    quantity: int
    line_total: int

@dataclass(slots=True)
class Order:
    id: int
    customer_id: int
    total_amount: int
    status: OrderStatus
    created_at: datetime
    items: list[OrderItem]
