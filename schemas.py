# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    user: str
    products: List[int]

    class Config:
        orm_mode = True

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    category_id: int

    class Config:
        orm_mode = True

# Category Response Schema
class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    user: str
    products: List[int]
    total_amount: float
    created_at: str

    class Config:
        orm_mode = True