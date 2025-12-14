# This file contains the Pydantic models (schemas) that are used for
# data validation and serialization. These are separate from the
# SQLAlchemy ORM models.

from pydantic import BaseModel
from typing import List, Optional

# --- Item Schemas ---

class ItemBase(BaseModel):
    """
    Base schema for an item. Contains fields that are common for
    both creating and reading items.
    """
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    """
    Schema for creating an item. Inherits from ItemBase.
    This schema is used in the request body when creating a new item.
    """
    pass # No extra fields needed for creation in this case.

class Item(ItemBase):
    """
    Schema for reading an item. Inherits from ItemBase.
    This schema is used in the response body.
    """
    id: int
    owner_id: int

    # `orm_mode = True` tells Pydantic to read the data even if it is not a dict,
    # but an ORM model (or any other arbitrary object with attributes).
    # This allows Pydantic to work with SQLAlchemy objects.
    class Config:
        orm_mode = True

# --- User Schemas ---

class UserBase(BaseModel):
    """
    Base schema for a user.
    """
    email: str

class UserCreate(UserBase):
    """
    Schema for creating a user.
    """
    password: str

class User(UserBase):
    """
    Schema for reading a user.
    """
    id: int
    is_active: bool
    items: List[Item] = [] # The response will include the user's items.

    class Config:
        orm_mode = True
