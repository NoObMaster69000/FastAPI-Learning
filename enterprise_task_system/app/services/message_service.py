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
