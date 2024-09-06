

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship



SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mypassword@db:5432/mydatabase"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    category = Column(String)
    stock_quantity = Column(Integer)
    rating = Column(Float)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    address = Column(String)
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    product_ids = Column(JSON)
    total_amount = Column(Float)
    status = Column(String)
    created_at = Column(DateTime)
    user = relationship("User", back_populates="orders")


