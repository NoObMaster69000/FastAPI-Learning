# enterprise_task_system/app/schemas/message.py

import uuid
from pydantic import BaseModel

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    task_id: uuid.UUID

class Message(MessageBase):
    id: uuid.UUID
    task_id: uuid.UUID

    model_config = {"from_attributes": True}
