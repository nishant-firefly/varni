from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    stock_quantity: int
    rating: Optional[float] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: str
    address: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    orders: List['Order'] = []

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int
    product_ids: str  # Ideally this should be a List[int], but depends on your design
    total_amount: float
    status: str
    created_at: datetime

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True
