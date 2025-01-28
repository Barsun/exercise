import pytest
from app import app
import sqlite3

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_item_valid_input(client):
    response = client.post('/items', json={
        'name': 'Test Item',
        'description': 'This is a test item'
    })
    assert response.status_code == 201
    assert b"Item added successfully" in response.data

def test_add_item_missing_fields(client):
    response = client.post('/items', json={
        'name': 'Test Item'
    })
    assert response.status_code == 400
    assert b"Missing required fields" in response.data

def test_add_item_invalid_types(client):
    response = client.post('/items', json={
        'name': 123,
        'description': 'This is a test item'
    })
    assert response.status_code == 400
    assert b"Fields 'name' and 'description' must be strings" in response.data