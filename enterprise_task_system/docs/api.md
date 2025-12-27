# API

The API layer is the entry point to the application. It's responsible for handling HTTP requests, validating incoming data, and returning HTTP responses. The API layer is located in the `app/api` directory.

## `app.schemas`

The `app/schemas` directory contains the Pydantic schemas for the application. These schemas are used to validate and serialize the data that is sent to and from the API.

### `task.py`

This module defines the Pydantic schemas for tasks.

```python
# enterprise_task_system/app/schemas/task.py

import uuid
from pydantic import BaseModel, computed_field
from datetime import datetime
from .user import User

# --- Task Schemas ---

# Shared properties
class TaskBase(BaseModel):
    title: str
    description: str | None = None

# Properties to receive on task creation
class TaskCreate(TaskBase):
    pass

# Properties to receive on task update
class TaskUpdate(TaskBase):
    status: str | None = None

# Properties shared by models stored in DB
class TaskInDBBase(TaskBase):
    id: uuid.UUID
    created_at: datetime
    owner_id: uuid.UUID

    model_config = {"from_attributes": True}

# Properties to return to client
class Task(TaskInDBBase):
    owner: User

    @computed_field
    @property
    def work_id_str(self) -> str:
        return self.work_id.work_id_str

# Additional properties stored in DB
class TaskInDB(TaskInDBBase):
    pass
```

- **`TaskBase`:** A base class that defines the common properties of a task.
- **`TaskCreate` and `TaskUpdate`:** Schemas for creating and updating tasks. They inherit from `TaskBase`.
- **`TaskInDBBase`:** A base class for tasks that are stored in the database. It includes the `id`, `created_at`, and `owner_id` fields. The `model_config = {"from_attributes": True}` setting tells Pydantic to create the model from a SQLAlchemy model object.
- **`Task`:** The schema for a task that is returned to the client. It includes the `owner` and `work_id_str` fields. The `work_id_str` is a `computed_field` that gets its value from the `work_id` relationship.

## `app.api.deps`

The `app.api.deps` module defines the dependencies for the API. These dependencies are used to inject common functionality into the API endpoints, such as getting a database session or getting the current user.

```python
# enterprise_task_system/app/api/deps.py

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, schemas
from app.config import settings
from app.db.session import SessionLocal
from app.core import security
from app.repositories.user_repository import user_repository

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.user.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.token.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = user_repository.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

- **`get_db`:** A dependency that provides a database session for each request. It uses a `try...finally` block to ensure that the session is always closed, even if there is an error.
- **`get_current_user`:** A dependency that gets the current user from the JWT token. It decodes the token, validates it, and then gets the user from the database.

## `app.api.v1.endpoints`

The `app.api.v1.endpoints` directory contains the API endpoints for the application.

### `tasks.py`

This module defines the API endpoints for tasks.

```python
# enterprise_task_system/app/api/v1/endpoints/tasks.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from typing import List

from app import models, schemas
from app.api import deps
from app.services.task_service import task_service
from app.repositories.task_repository import task_repository

router = APIRouter()


@router.get("/", response_model=List[schemas.task.Task])
def read_tasks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_user),
) -> List[models.task.Task]:
    """
    Retrieve tasks.
    """
    tasks = task_repository.get_multi_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return tasks


@router.post("/", response_model=schemas.task.Task)
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: schemas.task.TaskCreate,
    current_user: models.user.User = Depends(deps.get_current_user),
) -> models.task.Task:
    """
    Create new task.
    """
    task = task_service.create_task(db=db, obj_in=task_in, owner=current_user)
    return task
```

- **`read_tasks`:** An endpoint to get a list of tasks for the current user. It uses the `get_current_user` dependency to get the current user and the `TaskRepository` to get the tasks.
- **`create_task`:** An endpoint to create a new task. It uses the `get_current_user` dependency to get the current user and the `TaskService` to create the task. The `response_model` argument tells FastAPI to use the `Task` schema to serialize the response.
