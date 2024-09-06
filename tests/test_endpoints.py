from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_product():
    response = client.post("/products/", json={
        "id": "12345",
        "name": "Smartphone",
        "description": "A high-quality smartphone",
        "price": 699.99,
        "category": "Electronics",
        "stock_quantity": 50,
        "rating": 4.5
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Product created successfully"}

# Similarly, write tests for other CRUD operations
