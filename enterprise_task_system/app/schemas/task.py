# enterprise_task_system/app/schemas/task.py

import uuid
from pydantic import BaseModel, computed_field
from datetime import datetime
from .user import User

# --- Task Schemas ---

# Shared properties
class TaskBase(BaseModel):
    title: str
    description: str | None = None

# Properties to receive on task creation
class TaskCreate(TaskBase):
    pass

# Properties to receive on task update
class TaskUpdate(TaskBase):
    status: str | None = None

# Properties shared by models stored in DB
class TaskInDBBase(TaskBase):
    id: uuid.UUID
    created_at: datetime
    owner_id: uuid.UUID

    model_config = {"from_attributes": True}

# Properties to return to client
class Task(TaskInDBBase):
    owner: User

    @computed_field
    @property
    def work_id_str(self) -> str:
        return self.work_id.work_id_str

# Additional properties stored in DB
class TaskInDB(TaskInDBBase):
    pass
