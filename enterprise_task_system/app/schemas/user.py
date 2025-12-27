# enterprise_task_system/app/schemas/user.py

import uuid
from pydantic import BaseModel, EmailStr

# --- User Schemas ---

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: str

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = None

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: uuid.UUID
    is_active: bool

    model_config = {"from_attributes": True}

# Properties to return to client
class User(UserInDBBase):
    model_config = {"from_attributes": True}

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
