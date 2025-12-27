# enterprise_task_system/tests/integration/test_api/test_login.py

from fastapi.testclient import TestClient
from app.config import settings
from app.schemas.user import UserCreate
from app.repositories.user_repository import user_repository

def test_get_access_token(client: TestClient, db_session):
    # Create a user
    user_in = UserCreate(email="test@example.com", password="password", username="testuser")
    user_repository.create(db_session, obj_in=user_in)

    login_data = {
        "username": "test@example.com",
        "password": "password",
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
