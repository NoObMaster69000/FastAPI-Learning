# enterprise_task_system/app/repositories/work_id_repository.py

from sqlalchemy.orm import Session
from app.models.work_id import WorkID
from app.repositories.base import BaseRepository

class WorkIDRepository(BaseRepository[WorkID]):
    def get_by_work_id_str(self, db: Session, *, work_id_str: str) -> WorkID | None:
        return db.query(WorkID).filter(WorkID.work_id_str == work_id_str).first()

work_id_repository = WorkIDRepository(WorkID)
