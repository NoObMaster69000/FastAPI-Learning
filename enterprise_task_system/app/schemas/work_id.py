# enterprise_task_system/app/schemas/work_id.py

import uuid
from pydantic import BaseModel

class WorkIDBase(BaseModel):
    work_id_str: str

class WorkIDCreate(WorkIDBase):
    task_id: uuid.UUID

class WorkID(WorkIDBase):
    id: uuid.UUID
    task_id: uuid.UUID

    model_config = {"from_attributes": True}
