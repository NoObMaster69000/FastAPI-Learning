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
