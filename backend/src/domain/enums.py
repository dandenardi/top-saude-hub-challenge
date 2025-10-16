from enum import StrEnum

class OrderStatus(StrEnum):
    CREATED = "CREATED"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
