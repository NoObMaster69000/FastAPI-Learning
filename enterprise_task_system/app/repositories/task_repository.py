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

    def remove(self, db: Session, *, id: uuid.UUID) -> Task:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

task_repository = TaskRepository(Task)
