# enterprise_task_system/scripts/generate_sample_data.py

import logging

from app.db.session import SessionLocal
from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate
from app.services.task_service import task_service
from app.schemas.task import TaskCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_sample_data() -> None:
    logger.info("Creating sample data")
    db = SessionLocal()

    # Create a sample user
    user = user_repository.get_by_email(db, email="test@example.com")
    if not user:
        user_in = UserCreate(email="test@example.com", password="password", username="testuser")
        user = user_repository.create(db, obj_in=user_in)
        logger.info("Sample user created")

    # Create a sample task
    task_in = TaskCreate(title="Sample Task", description="This is a sample task.")
    task_service.create_task(db, obj_in=task_in, owner=user)
    logger.info("Sample task created")

    db.close()
    logger.info("Sample data created")

if __name__ == "__main__":
    generate_sample_data()
