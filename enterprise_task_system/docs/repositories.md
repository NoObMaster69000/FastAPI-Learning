# Repositories

The repository pattern is a design pattern that abstracts the data layer, making it easier to manage and test. In this project, the repositories are located in the `app/repositories` directory.

## `base.py`

The `base.py` module defines a `BaseRepository` class that provides generic CRUD (Create, Read, Update, Delete) methods. Other repositories in the application can inherit from this class to get basic CRUD functionality.

```python
# enterprise_task_system/app/repositories/base.py

from typing import Any, Generic, Type, TypeVar

from sqlalchemy.orm import Session
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        Base class for data access logic.

        :param model: A SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
```

- **`ModelType`:** A `TypeVar` that allows the `BaseRepository` to be generic. This means it can work with any SQLAlchemy model.
- **`__init__`:** The constructor takes a SQLAlchemy model class as an argument.
- **`get`:** A generic method to get a single object by its ID.
- **`create`:** A generic method to create a new object.
- **`remove`:** A generic method to delete an object by its ID.

## `task_repository.py`

The `task_repository.py` module defines the `TaskRepository` class, which is responsible for all database operations related to tasks.

```python
# enterprise_task_system/app/repositories/task_repository.py

from app.models.task import Task
from app.repositories.base import BaseRepository
from sqlalchemy.orm import Session, joinedload
import uuid
from typing import List
from app.schemas.task import TaskUpdate

class TaskRepository(BaseRepository[Task]):
    def get(self, db: Session, id: uuid.UUID) -> Task | None:
        return db.query(self.model).options(joinedload(Task.work_id), joinedload(Task.owner)).filter(self.model.id == id).first()

    def get_multi_by_owner(
        self, db: Session, *, owner_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        return (
            db.query(self.model)
            .filter(Task.owner_id == owner_id)
            .options(joinedload(Task.work_id), joinedload(Task.owner))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: dict) -> Task:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return self.get(db, id=db_obj.id)

    def update(self, db: Session, *, db_obj: Task, obj_in: TaskUpdate) -> Task:
        db_obj.title = obj_in.title
        db_obj.description = obj_in.description
        db_obj.status = obj_in.status
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return self.get(db, id=db_obj.id)

task_repository = TaskRepository(Task)
```

- **`get` and `get_multi_by_owner`:** These methods override the generic `get` and add a new method to get multiple tasks by their owner. They also use `joinedload` to eagerly load the `work_id` and `owner` relationships, which is a performance optimization.
- **`create` and `update`:** These methods override the generic methods to return the object with the relationships loaded.

## Other Repositories

The other repositories (`user_repository.py`, `work_id_repository.py`, `message_repository.py`) are similar to the `task_repository.py`. They inherit from the `BaseRepository` and add any specific methods they need.
