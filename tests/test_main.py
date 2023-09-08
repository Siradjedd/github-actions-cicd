import sys
import pytest
from flask import json

# Add the project root directory to the Python path
sys.path.append('/home/siradjedd/github-actions-cicd')

from src.main import app, db, TodoList

@pytest.fixture
def client():
    # Create a test client for the Flask app
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_todo(client):
    # Test creating a new todo
    response = client.post('/todo-create', json={"todo": "Test Todo"})
    assert response.status_code == 200
    assert response.json == {"201": "Todo created successfully"}

def test_get_all_todos(client):
    # Test getting all todos
    response = client.get('/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_update_todo(client):
    # Test updating a todo
    # Create a test todo first
    client.post('/todo-create', json={"todo": "Test Todo"})
    
    # Update the todo
    response = client.put('/update/4', json={"todo": "Updated Todo"})
    assert response.status_code == 200
    assert response.json == {"200": "Updated successfully"}
