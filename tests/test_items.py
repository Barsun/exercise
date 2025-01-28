import pytest
from app import create_app
from app.database import db
from app.database.models import Item

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
@pytest.fixture
def client(app):
    return app.test_client()

def test_create_item(client):
    response = client.post("/api/v1/items", json={"name": "Test Item", "description": "Test Description"})
    assert response.status_code == 201
    assert "id" in response.json

def test_get_all_items(client):
    # Create an item first
    client.post("/api/v1/items", json={"name": "Test Item 1", "description": "Description 1"})
    client.post("/api/v1/items", json={"name": "Test Item 2", "description": "Description 2"})

    response = client.get("/api/v1/items")
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_item(client):
    # Create an item first
    create_response = client.post("/api/v1/items", json={"name": "Test Item", "description": "Test Description"})
    item_id = create_response.json["id"]

    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json["name"] == "Test Item"

def test_update_item(client):
    # Create an item first
    create_response = client.post("/api/v1/items", json={"name": "Test Item", "description": "Test Description"})
    item_id = create_response.json["id"]

    response = client.put(f"/api/v1/items/{item_id}", json={"name": "Updated Item", "description": "Updated Description"})
    assert response.status_code == 200
    assert response.json["message"] == "Item updated"

    # Verify the update
    get_response = client.get(f"/api/v1/items/{item_id}")
    assert get_response.json["name"] == "Updated Item"

def test_delete_item(client):
    # Create an item first
    create_response = client.post("/api/v1/items", json={"name": "Test Item", "description": "Test Description"})
    item_id = create_response.json["id"]

    response = client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json["message"] == "Item deleted"

    # Verify the deletion
    get_response = client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 404