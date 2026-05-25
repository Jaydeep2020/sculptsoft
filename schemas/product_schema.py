from pydantic import BaseModel
from typing import Optional
from models.enums import CategoryType
from datetime import date

class ProductCreate(BaseModel):
    name: str
    category: CategoryType
    price: float
    warranty_month: Optional[int] = None
    expiry_date: Optional[date] = None

class ProductResponse(BaseModel):
    name: str
    category: CategoryType
    price: float

    class Config:
        from_attributes = True

