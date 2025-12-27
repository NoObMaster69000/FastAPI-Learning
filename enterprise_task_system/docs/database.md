# Database

The `app/db` and `app/models` directories contain all the database-related code. This includes the database session setup, the base class for the SQLAlchemy models, and the models themselves.

## `app.db.base_class`

This module defines the `Base` class that all SQLAlchemy models in the application inherit from.

```python
# enterprise_task_system/app/db/base_class.py

from sqlalchemy.orm import declarative_base

Base = declarative_base()
```

Using a declarative base class allows SQLAlchemy to map the Python objects to database tables. It also enables Alembic to automatically detect changes to the models and generate database migrations.

## `app.db.session`

This module is responsible for creating the database engine and the `SessionLocal` class.

```python
# enterprise_task_system/app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

- **`engine`:** The `create_engine` function creates a new SQLAlchemy engine, which is the entry point to the database. The `pool_pre_ping=True` argument tells the engine to check the health of a connection before using it, which helps to prevent issues with stale connections.
- **`SessionLocal`:** The `sessionmaker` function returns a class that can be used to create new database sessions. Each instance of the `SessionLocal` class will be a new database session.

## `app.models`

The `app/models` directory contains the SQLAlchemy models for the application. Each model corresponds to a table in the database.

### `user.py`

This model represents a user in the system.

```python
# enterprise_task_system/app/models/user.py

import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)

    tasks = relationship("Task", back_populates="owner")
```

- **`__tablename__`:** This attribute tells SQLAlchemy the name of the table to use in the database.
- **`id`:** The primary key for the table. It's a UUID, which is a good choice for primary keys in a distributed system.
- **`username` and `email`:** Basic user information. The `email` is unique.
- **`hashed_password`:** The user's password, which is hashed for security.
- **`is_active`:** A boolean flag to indicate if the user is active.
- **`tasks`:** A relationship to the `Task` model. This allows you to access a user's tasks using `user.tasks`. The `back_populates` argument tells SQLAlchemy to link this relationship with the `owner` relationship on the `Task` model.

### `task.py`

This model represents a task in the system.

```python
# enterprise_task_system/app/models/task.py

import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

from app.db.base_class import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")

    work_id = relationship("WorkID", back_populates="task", uselist=False)
    messages = relationship("Message", back_populates="task")
```

- **`owner_id` and `owner`:** These define the relationship to the `User` model. The `owner_id` is a foreign key to the `users` table.
- **`work_id`:** A one-to-one relationship to the `WorkID` model. The `uselist=False` argument tells SQLAlchemy that this is a one-to-one relationship.
- **`messages`:** A one-to-many relationship to the `Message` model.

### `work_id.py`

This model represents a work ID in the system.

```python
# enterprise_task_system/app/models/work_id.py

import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class WorkID(Base):
    __tablename__ = "work_ids"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_id_str = Column(String, unique=True, index=True, nullable=False)

    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="work_id")
```

- **`work_id_str`:** The unique, human-readable work ID string.
- **`task_id` and `task`:** These define the one-to-one relationship to the `Task` model.

### `message.py`

This model represents a message in the system.

```python
# enterprise_task_system/app/models/message.py

import uuid
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)

    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="messages")
```
- **`content`:** The content of the message.
- **`task_id` and `task`:** These define the relationship to the `Task` model.
