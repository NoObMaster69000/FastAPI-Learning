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
