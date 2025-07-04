import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

def register_user(client, username, password):
    return client.post("/auth/register", data={"username": username, "password": password})

def login_user(client, username, password):
    response = client.post("/auth/token", data={"username": username, "password": password})
    return response.json()["access_token"]
