from pydantic import BaseModel, Field
from typing import Literal, Optional

class PaginationIn(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=200)
    q: Optional[str] = None
    sort: str = "created_at:desc" 

SortDir = Literal["asc", "desc"]
