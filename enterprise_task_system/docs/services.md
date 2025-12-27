# Services

The service layer is where the business logic of the application resides. It's responsible for orchestrating the different parts of the application to perform a specific task. The services are located in the `app/services` directory.

## `task_service.py`

The `task_service.py` module defines the `TaskService` class, which is responsible for all business logic related to tasks.

```python
# enterprise_task_system/app/services/task_service.py

from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate
from app.repositories.task_repository import task_repository
from app.services.work_id_service import work_id_service
from app.services.message_service import message_service

class TaskService:
    def create_task(self, db: Session, *, obj_in: TaskCreate, owner: User) -> Task:
        """
        Create a new task and orchestrate related operations.

        This service method handles the business logic for:
        1. Creating the task record in the database.
        2. Calling the WorkIDService to generate and assign a unique work ID.
        3. Calling the MessageService to create the initial notification message.

        Args:
            db: The SQLAlchemy database session.
            obj_in: The Pydantic schema containing the task creation data.
            owner: The user who is creating the task.

        Returns:
            The newly created Task object.
        """
        # 1. Create the task
        db_obj = task_repository.create(db, obj_in={"title": obj_in.title, "description": obj_in.description, "owner_id": owner.id})

        # 2. Generate and assign a work ID
        work_id = work_id_service.generate_and_assign_work_id(db, task=db_obj)

        # 3. Create the initial message
        message_service.create_task_creation_message(db, task=db_obj, user=owner, work_id=work_id)

        return db_obj

task_service = TaskService()
```

- **`create_task`:** This method orchestrates the creation of a new task. It calls the `TaskRepository` to create the task, the `WorkIDService` to generate and assign a work ID, and the `MessageService` to create the initial message.

## `work_id_service.py`

The `work_id_service.py` module defines the `WorkIDService` class, which is responsible for generating and assigning work IDs.

```python
# enterprise_task_system/app/services/work_id_service.py

from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_fixed

from app.utils.work_id_generator import generate_work_id
from app.repositories.work_id_repository import work_id_repository
from app.models.task import Task
from app.models.work_id import WorkID

class WorkIDService:
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def generate_and_assign_work_id(self, db: Session, *, task: Task) -> WorkID:
        """
        Generates a unique work ID and assigns it to a task.

        This method uses a retry mechanism to handle the rare case of a work ID
        collision. If a generated ID already exists in the database, it will
        retry up to 3 times to generate a new, unique one.

        Args:
            db: The SQLAlchemy database session.
            task: The task to which the work ID should be assigned.

        Returns:
            The created WorkID object.
        """
        work_id_str = generate_work_id()

        # Check if the generated work ID already exists.
        existing_work_id = work_id_repository.get_by_work_id_str(db, work_id_str=work_id_str)

        if existing_work_id:
            # If it exists, raise an exception to trigger a retry.
            raise ValueError("Work ID collision detected. Retrying...")

        # If the work ID is unique, create and assign it.
        work_id_obj = work_id_repository.create(
            db, obj_in={"work_id_str": work_id_str, "task_id": task.id}
        )

        return work_id_obj

work_id_service = WorkIDService()
```

- **`generate_and_assign_work_id`:** This method uses the `tenacity` library to automatically retry the operation if a work ID collision is detected. This is a good practice for ensuring the robustness of the system.

## `message_service.py`

The `message_service.py` module defines the `MessageService` class, which is responsible for creating and storing messages.

```python
# enterprise_task_system/app/services/message_service.py

from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.models.work_id import WorkID
from app.models.message import Message
from app.utils.message_formatter import format_task_creation_message
from app.repositories.message_repository import message_repository

class MessageService:
    def create_task_creation_message(
        self,
        db: Session,
        *,
        task: Task,
        user: User,
        work_id: WorkID
    ) -> Message:
        """
        Creates and stores a formatted message for a new task.

        This service uses the `message_formatter` to generate the content
        and then saves it to the database using the `MessageRepository`.

        Args:
            db: The SQLAlchemy database session.
            task: The newly created task.
            user: The user who owns the task.
            work_id: The work ID assigned to the task.

        Returns:
            The created Message object.
        """
        formatted_content = format_task_creation_message(
            task=task, user=user, work_id=work_id
        )

        message_obj = message_repository.create(
            db, obj_in={"content": formatted_content, "task_id": task.id}
        )

        return message_obj

message_service = MessageService()
```
- **`create_task_creation_message`:** This method uses the `message_formatter` utility to generate the message content and then saves it to the database.
