# enterprise_task_system/app/schemas/common.py

from pydantic import BaseModel

class Msg(BaseModel):
    """
    A schema for returning simple messages to the client.
    """
    msg: str
