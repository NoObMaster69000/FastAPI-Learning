# enterprise_task_system/scripts/init_db.py

import logging

from app.db.session import SessionLocal
from app.db.base import Base
from app.db.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    # Tables should be created with Alembic, so this is just for dev
    logger.info("Creating initial data")
    db = SessionLocal()
    Base.metadata.create_all(bind=engine)
    db.close()
    logger.info("Initial data created")


if __name__ == "__main__":
    init_db()
