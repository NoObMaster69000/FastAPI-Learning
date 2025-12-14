# To run these tests:
# 1. Make sure you have `pytest` and `requests` installed:
#    pip install pytest requests httpx
# 2. cd into the project root directory.
# 3. Run `pytest` in your terminal.

import pytest
from fastapi.testclient import TestClient
from main import app, get_current_user

# --- Pytest Fixtures for Test Clients ---

# Using fixtures is the best practice for managing setup and teardown in tests.
# This ensures that each test runs in a clean, isolated environment.

@pytest.fixture
def client():
    """
    A fixture that provides a TestClient with the original dependencies.
    This is used for testing the actual logic of the dependencies (e.g., error handling).
    """
    # Ensure no overrides are present from other tests.
    app.dependency_overrides = {}
    with TestClient(app) as c:
        yield c

@pytest.fixture
def client_with_auth_override():
    """
    A fixture that provides a TestClient where the authentication dependency
    is overridden. This is used to test the logic of the endpoint *without*
    triggering the actual authentication logic.
    """
    # This is our mock/override function. It takes no arguments.
    async def override_get_current_user():
        return {"username": "testuser"}

    # Apply the override.
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c

    # The fixture automatically cleans up the override after the test is done.
    app.dependency_overrides = {}


# --- Basic Endpoint Tests ---

def test_read_root(client):
    """ Tests the root endpoint. """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_read_item(client):
    """ Tests an endpoint with path and query parameters. """
    response = client.get("/items/42?q=somequery")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": "somequery"}


# --- Testing Authentication Logic (with original dependency) ---

def test_read_current_user_no_token(client):
    """
    Tests the protected endpoint without providing the required header.
    We expect a 422 Unprocessable Entity error because the dependency requirement is not met.
    """
    response = client.get("/users/me")
    assert response.status_code == 422

def test_read_current_user_invalid_token(client):
    """
    Tests the protected endpoint with an invalid token.
    We expect a 400 Bad Request error, as defined in the original dependency.
    """
    response = client.get("/users/me", headers={"X-Token": "invalid-token"})
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}

def test_read_current_user_valid_token(client):
    """
    Tests the protected endpoint with a valid token.
    This tests the successful path of the original dependency.
    """
    response = client.get("/users/me", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    assert response.json() == {"username": "fakeuser"}


# --- Testing Endpoint Logic (with overridden dependency) ---

def test_read_current_user_with_override(client_with_auth_override):
    """
    Tests the protected endpoint using the client with the auth dependency overridden.
    - We don't need to provide any headers because the overriding dependency
      doesn't have any parameters.
    - This allows us to test the endpoint's logic in isolation from the auth logic.
    """
    response = client_with_auth_override.get("/users/me")
    assert response.status_code == 200
    assert response.json() == {"username": "testuser"}
