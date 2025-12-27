# enterprise_task_system/app/repositories/message_repository.py

from app.models.message import Message
from app.repositories.base import BaseRepository

class MessageRepository(BaseRepository[Message]):
    pass

message_repository = MessageRepository(Message)
