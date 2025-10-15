from pydantic import BaseModel, Field, EmailStr

class CustomerIn(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    document: str

class CustomerOut(CustomerIn):
    id: int
