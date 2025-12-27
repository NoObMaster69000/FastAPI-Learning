# enterprise_task_system/tests/integration/test_api/test_tasks.py

from fastapi.testclient import TestClient
from app.config import settings
from app.schemas.user import UserCreate
from app.repositories.user_repository import user_repository

def get_superuser_token_headers(client: TestClient, db_session) -> dict[str, str]:
    # Create a user
    user_in = UserCreate(email="test@example.com", password="password", username="testuser")
    user = user_repository.get_by_email(db_session, email="test@example.com")
    if not user:
        user_repository.create(db_session, obj_in=user_in)

    login_data = {
        "username": "test@example.com",
        "password": "password",
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers

def test_create_task(client: TestClient, db_session):
    headers = get_superuser_token_headers(client, db_session)
    response = client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers=headers,
        json={"title": "Test Task", "description": "Test Description"},
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == "Test Task"
    assert content["description"] == "Test Description"
    assert "id" in content
    assert "owner_id" in content

def test_read_task(client: TestClient, db_session):
    headers = get_superuser_token_headers(client, db_session)
    # First create a task
    response = client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers=headers,
        json={"title": "Test Task", "description": "Test Description"},
    )
    task_id = response.json()["id"]

    # Now read it
    response = client.get(
        f"{settings.API_V1_STR}/tasks/{task_id}",
        headers=headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == "Test Task"
    assert content["description"] == "Test Description"
    assert content["id"] == task_id
