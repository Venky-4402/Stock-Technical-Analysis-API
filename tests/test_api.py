from fastapi.testclient import TestClient
from app.main import app
import uuid
client = TestClient(app)
def test_register_and_login(client):
    username = f"testuser_{uuid.uuid4().hex[:8]}"  # Unique username
    password = "testpass"
    response = client.post("/auth/register", data={"username": username, "password": password})
    assert response.status_code == 200
    response = client.post("/auth/token", data={"username": username, "password": password})
    assert response.status_code == 200
    assert "access_token" in response.json()
