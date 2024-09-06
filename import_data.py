


import json
import traceback
from sqlalchemy.orm import Session
from api.models import Product, User, Order
from api.database import SessionLocal

# Load JSON data
def load_json(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading file {file_name}: {e}")
        raise

def import_products(db: Session):
    products = load_json("data/products.json")
    for item in products:
        try:
            db_product = Product(
                id=int(item["id"]),  # Convert to integer if needed
                name=item["name"],
                description=item["description"],
                price=item["price"],
                category=item.get("category"),
                stock_quantity=item.get("stock_quantity"),
                rating=item.get("rating")
            )
            db.merge(db_product)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error importing product {item['id']}: {e}")
            print(traceback.format_exc())

def import_users(db: Session):
    users = load_json("data/users.json")
    for item in users:
        try:
            db_user = User(
                id=item["id"],  # Ensure this matches your schema
                name=item["name"],
                email=item["email"],
                address=item.get("address"),
                orders=[]  # Initialize empty list; populate orders separately if needed
            )
            db.merge(db_user)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error importing user {item['id']}: {e}")
            print(traceback.format_exc())

def import_orders(db: Session):
    orders = load_json("data/orders.json")
    for item in orders:
        try:
            order_id = item["id"]
            user_id = item["user_id"]
            
            # Check if user_id and product_ids exist in the database
            user_exists = db.query(User).filter(User.id == user_id).first()
            if not user_exists:
                print(f"Skipping order {item['id']} with non-existent user ID: {user_id}")
                continue

            product_ids = item.get("product_ids", [])
            products_exist = all(db.query(Product).filter(Product.id == pid).first() for pid in product_ids)
            if not products_exist:
                print(f"Skipping order {item['id']} with non-existent product IDs: {product_ids}")
                continue

            db_order = Order(
                id=order_id,
                user_id=user_id,
                product_ids=product_ids,
                total_amount=item["total_amount"],
                status=item["status"],
                created_at=item["created_at"]
            )
            db.merge(db_order)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error importing order {item['id']}: {e}")
            print(traceback.format_exc())

if __name__ == "__main__":
    db = SessionLocal()
    try:
        import_products(db)
        import_users(db)
        import_orders(db)
    finally:
        db.close()
