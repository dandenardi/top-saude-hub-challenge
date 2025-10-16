from pydantic import BaseModel, EmailStr, constr, ConfigDict
from datetime import datetime
from typing import Optional

DocStr = constr(strip_whitespace=True, min_length=5, max_length=32)

class CustomerIn(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=200)
    email: EmailStr
    document: DocStr

class CustomerUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=200)] = None
    email: Optional[EmailStr] = None
    document: Optional[DocStr] = None

class CustomerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    document: str
    created_at: datetime
