# Testing

The tests for the application are located in the `tests` directory. The tests are divided into three categories: unit, integration, and end-to-end.

## Unit Tests

Unit tests are used to test individual components of the application in isolation. They are located in the `tests/unit` directory.

### `test_work_id_generator.py`

This module contains a unit test for the `work_id_generator` utility.

```python
# enterprise_task_system/tests/unit/test_utils/test_work_id_generator.py

from app.utils.work_id_generator import generate_work_id

def test_generate_work_id():
    """
    Test that the work ID generator returns a string in the correct format.
    """
    work_id = generate_work_id()

    assert isinstance(work_id, str)
    assert work_id.startswith("TSK-")
    parts = work_id.split("-")
    assert len(parts) == 3
    assert parts[1].isdigit()
    assert len(parts[2]) == 4
```

## Integration Tests

Integration tests are used to test the interaction between different components of the application. They are located in the `tests/integration` directory.

### `test_login.py`

This module contains an integration test for the login flow.

```python
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
```

## `conftest.py`

The `conftest.py` file in the `tests` directory contains the test setup code.

```python
# enterprise_task_system/tests/conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
from fastapi.testclient import TestClient

# Add the project root to the sys.path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.api.deps import get_db
from app.db.base_class import Base
import app.models.user
import app.models.task
import app.models.work_id
import app.models.message

SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db_session():
    """
    Creates a new database session for a test.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("/tmp/test.db"):
            os.remove("/tmp/test.db")

@pytest.fixture(scope="function")
def client(db_session):
    """
    Creates a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c
```

- **`db_session` fixture:** This fixture creates a new database session for each test and then cleans up the database after the test is finished. It uses an in-memory SQLite database to ensure that the tests are fast and isolated.
- **`client` fixture:** This fixture creates a new FastAPI `TestClient` for each test. It also overrides the `get_db` dependency to use the `db_session` fixture.

## Running the Tests

To run the tests, you first need to install the test dependencies.

```bash
pip install -r requirements.txt
```

Then, you can run the tests using `pytest`.

```bash
cd enterprise_task_system
pytest
```
**Note:** There is a known issue with the test setup that causes a `ModuleNotFoundError` when running `pytest` from the root of the `enterprise_task_system` directory. This is due to the way the Python path is configured. A workaround is to run the tests from the parent directory.
