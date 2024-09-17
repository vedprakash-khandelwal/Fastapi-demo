# test_main.py
from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_create_category():
    response = client.post("/categories/", json={"name": "Electronics", "description": "Devices"})
    assert response.status_code == 200
    assert response.json()["name"] == "Electronics"

def test_create_product():
    response = client.post("/products/", json={
        "name": "Laptop",
        "description": "Gaming Laptop",
        "price": 1500.0,
        "stock": 10,
        "category_id": 1
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"

def test_create_order_with_insufficient_stock():
    # Assuming there's a product with ID 1 with 0 stock
    response = client.post("/orders/", json={
        "user": "user1",
        "products": [6]
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Product iPhone 16 is out of stock."