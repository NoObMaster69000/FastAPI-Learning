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
