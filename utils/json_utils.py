import json
from pathlib import Path

# Directory where your JSON data files are stored
DATA_DIR = Path("data")

def load_products():
    """Load all products from the products.json file."""
    with open(DATA_DIR / "products.json", "r") as file:
        return json.load(file)

def save_products(products):
    """Save all products to the products.json file."""
    with open(DATA_DIR / "products.json", "w") as file:
        json.dump(products, file, indent=4)
