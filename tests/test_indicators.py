from app.db.session import get_db
from app.db.models import User
from tests.conftest import register_user, login_user

def set_user_tier(username, tier):
    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    user.tier = tier
    db.commit()
    db.close()

def test_free_user_cannot_access_rsi(client):
    username = "freeuser"
    password = "testpass"
    # Register and login
    client.post("/auth/register", data={"username": username, "password": password})
    token = login_user(client, username, password)
    set_user_tier(username, "free")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "symbol": "SIYSIL",
        "start_date": "2022-07-01",
        "end_date": "2023-03-31",
        "period": 14
    }
    response = client.post("/indicators/rsi", json=payload, headers=headers)
    assert response.status_code == 403
    assert "Only SMA and EMA allowed" in response.text

def test_exceeding_daily_limit_returns_429(client):
    username = "ratelimituser"
    password = "testpass"
    client.post("/auth/register", data={"username": username, "password": password})
    token = login_user(client, username, password)
    set_user_tier(username, "free")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "symbol": "SIYSIL",
        "start_date": "2022-07-01",
        "end_date": "2023-03-31",
        "window": 10
    }
    for _ in range(51):  # Free tier: 50/day
        response = client.post("/indicators/sma", json=payload, headers=headers)
    assert response.status_code == 429
    assert "requests per day reached" in response.text

def test_invalid_date_range_returns_403(client):
    username = "daterangeuser"
    password = "testpass"
    client.post("/auth/register", data={"username": username, "password": password})
    token = login_user(client, username, password)
    set_user_tier(username, "free")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "symbol": "SIYSIL",
        "start_date": "2022-07-01",
        "end_date": "2023-03-31",  # > 3 months for free tier
        "window": 10
    }
    response = client.post("/indicators/sma", json=payload, headers=headers)
    assert response.status_code == 403
    assert "Max 3 months of data allowed" in response.text
