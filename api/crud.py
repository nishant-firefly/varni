import json
from pathlib import Path
from sqlalchemy.orm import Session
from api.models import Product, User, Order
from api.database import SessionLocal

# Directory where your JSON data files are stored
DATA_DIR = Path("data")

# Utility functions for handling JSON operations
def load_json(file_name):
    """Load data from a JSON file."""
    with open(DATA_DIR / file_name, "r") as file:
        return json.load(file)

def save_json(file_name, data):
    """Save data to a JSON file."""
    with open(DATA_DIR / file_name, "w") as file:
        json.dump(data, file, indent=4)


# CRUD operations for Products in JSON
def get_product_json(product_id):
    products = load_json("products.json")
    return next((p for p in products if p["id"] == product_id), None)

def create_product_json(product_data):
    products = load_json("products.json")
    products.append(product_data)
    save_json("products.json", products)

def update_product_json(product_id, updated_data):
    products = load_json("products.json")
    for product in products:
        if product["id"] == product_id:
            product.update(updated_data)
            save_json("products.json", products)
            return product
    return None

def delete_product_json(product_id):
    products = load_json("products.json")
    products = [p for p in products if p["id"] != product_id]
    save_json("products.json", products)


# CRUD operations for Products in PostgreSQL
def get_product_db(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create_product_db(db: Session, product_data: dict):
    db_product = Product(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product_db(db: Session, product_id: int, updated_data: dict):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        for key, value in updated_data.items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
    return product

def delete_product_db(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product


# Example usage
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
