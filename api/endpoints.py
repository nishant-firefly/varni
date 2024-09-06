from fastapi import APIRouter, HTTPException
from typing import List
from api.schemas import Product, User, Order
from api.database import SessionLocal
from api.models import Product as DBProduct, User as DBUser, Order as DBOrder

router = APIRouter()

# Example endpoint to get all products
@router.get("/products/", response_model=List[Product])
def get_products():
    db = SessionLocal()
    products = db.query(DBProduct).all()
    return products

# Similarly, update other endpoints


# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session
# from api.models import User, Product, Order
# from api.models import SessionLocal

# app = FastAPI()

# # Dependency to get the SQLAlchemy session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/users")
# def read_users(db: Session = Depends(get_db)):
#     return db.query(User).all()

# @app.get("/products")
# def read_products(db: Session = Depends(get_db)):
#     return db.query(Product).all()

# @app.get("/orders")
# def read_orders(db: Session = Depends(get_db)):
#     return db.query(Order).all()
