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
