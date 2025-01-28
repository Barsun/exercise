from unittest.mock import patch, MagicMock
import pytest
from app import create_app
from app.database.models import Item

@pytest.fixture
def mock_db_session():
    # Create a MagicMock to substitute for the SQLAlchemy session
    mock_session = MagicMock()
    return mock_session

@pytest.fixture
def app(mock_db_session):
    app = create_app()
    app.config["TESTING"] = True

    # Patch the db.session to use our mock session
    with patch("app.database.db.session", mock_db_session):
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_item(client, mock_db_session):
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    new_item = Item(name="Test Item", description="Test Description")
    mock_db_session.add.side_effect = lambda item: setattr(item, "id", 1)

    response = client.post("/api/v1/items", json={"name": new_item.name, "description": new_item.description})
    
    assert response.status_code == 201
    assert "id" in response.json
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()

def test_get_all_items(client, mock_db_session):
    mock_db_session.query.return_value.all.return_value = [
        Item(name="Test Item 1", description="Description 1"),
        Item(name="Test Item 2", description="Description 2")
    ]

    response = client.get("/api/v1/items")
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_item(client, mock_db_session):
    expected_item = Item(name="Test Item", description="Test Description")
    expected_item.id = 1
    mock_db_session.query.return_value.get.return_value = expected_item

    response = client.get(f"/api/v1/items/{expected_item.id}")
    assert response.status_code == 200
    assert response.json["name"] == expected_item.name

def test_update_item(client, mock_db_session):
    existing_item = Item(name="Test Item", description="Test Description")
    existing_item.id = 1
    mock_db_session.query.return_value.get.return_value = existing_item

    response = client.put(f"/api/v1/items/{existing_item.id}", json={"name": "Updated Item", "description": "Updated Description"})
    assert response.status_code == 200
    assert response.json["message"] == "Item updated"

    # Check that the session was used correctly
    assert existing_item.name == "Updated Item"
    mock_db_session.commit.assert_called_once()

def test_delete_item(client, mock_db_session):
    existing_item = Item(name="Test Item", description="Test Description")
    existing_item.id = 1
    mock_db_session.query.return_value.get.return_value = existing_item

    response = client.delete(f"/api/v1/items/{existing_item.id}")
    assert response.status_code == 200
    assert response.json["message"] == "Item deleted"

    # Verify the deletion was registered
    mock_db_session.delete.assert_called_once_with(existing_item)
    mock_db_session.commit.assert_called_once()

    # Simulating item not found after delete
    mock_db_session.query.return_value.get.return_value = None
    get_response = client.get(f"/api/v1/items/{existing_item.id}")
    assert get_response.status_code == 404