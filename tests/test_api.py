import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api import app, get_db
from src.db import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def setup_data():
    client.post("/register", json={"username": "testuser", "password": "password123"})
    login_res = client.post("/login", json = {"username": "testuser", "password": "password123"})
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    task_data = {"description": "My first test task", "priority": "high"}  
    add_response = client.post("/tasks", json=task_data, headers=headers)

    return {
        "headers": headers,
        "add_response": add_response
    }

def test_register_user():
    response = client.post("/register", json={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfull registration"}

def test_login_user():
    client.post("/register", json={"username": "testuser", "password": "password123"})
    response = client.post("/login", json={"username": "testuser", "password": "password123"})
    
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_task():
    client.post("/register", json={"username": "testuser", "password": "password123"})
    login_res = client.post("/login", json={"username": "testuser", "password": "password123"})
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    task_data = {"description": "My first test task", "priority": "high"}
    
    response = client.post("/tasks", json=task_data, headers=headers)
    
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully created"
    assert "task_id" in response.json()

def test_delete_task():
    client.post("/register", json={"username": "testuser", "password": "password123"})
    login_res = client.post("/login", json = {"username": "testuser", "password": "password123"})
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    task_data = {"description": "My first test task", "priority": "high"}  
    response = client.post("/tasks", json=task_data, headers=headers)

    task_id = response.json()["task_id"]
    response = client.delete(f"/tasks/{task_id}", headers = headers)

    assert response.status_code == 200
    assert response.json()["message"] == f"Task {task_id} successfully deleted"

def test_update_desc(setup_data):   
    task_id = setup_data["add_response"].json()["task_id"]
    new_desc = {"description": "New text"}
    response = client.put(f"/tasks/{task_id}/description", json = new_desc, headers = setup_data["headers"])

    assert response.status_code == 200
    assert response.json()["message"] == f"Task {task_id} description successfully updated"

    get_response = client.get("/tasks", headers = setup_data["headers"])
    tasks_list = get_response.json()

    assert tasks_list[task_id - 1]["description"] == "New text"

def test_update_proirity(setup_data):
    task_id = setup_data["add_response"].json()["task_id"]
    new_prior = {"priority": "medium"}
    response = client.put(f"/tasks/{task_id}/priority", json = new_prior, headers = setup_data["headers"])

    assert response.status_code == 200
    assert response.json()["message"] == f"Task {task_id} priority successfully updated"

    get_response = client.get("/tasks", headers = setup_data["headers"])
    tasks_list = get_response.json()

    assert tasks_list[task_id - 1]["priority"] == "medium"

def test_update_status(setup_data):
    task_id = setup_data["add_response"].json()["task_id"]
    new_status = {"status": "in-progress"}
    response = client.put(f"/tasks/{task_id}/status", json = new_status, headers = setup_data["headers"])

    assert response.status_code == 200
    assert response.json()["message"] == f"Task {task_id} status successfully updated"

    get_response = client.get("/tasks", headers = setup_data["headers"])
    tasks_list = get_response.json()

    assert tasks_list[task_id - 1]["status"] == "in-progress"

def test_get_tasks(setup_data):
    task_id = setup_data["add_response"].json()["task_id"]

    get_response = client.get("/tasks", headers = setup_data["headers"])
    tasks_list = get_response.json()

    assert len(tasks_list) == 1
    assert tasks_list[task_id - 1]["id"] == 1
    assert tasks_list[task_id - 1]["description"] == "My first test task"
    assert tasks_list[task_id - 1]["status"] == "todo"
    assert tasks_list[task_id - 1]["priority"] == "high"