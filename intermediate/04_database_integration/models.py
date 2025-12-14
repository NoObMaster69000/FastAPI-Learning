# This file contains the SQLAlchemy ORM models, which represent
# the tables in your database.

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base # Import the Base from our database.py

class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    """
    __tablename__ = "users" # The name of the table in the database.

    # --- Columns ---
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # --- Relationships ---
    # This creates a relationship between the User and Item models.
    # When you access `user.items`, SQLAlchemy will fetch the items
    # associated with that user from the 'items' table.
    items = relationship("Item", back_populates="owner")

class Item(Base):
    """
    SQLAlchemy model for the 'items' table.
    """
    __tablename__ = "items"

    # --- Columns ---
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id")) # Foreign key to the 'users' table.

    # --- Relationships ---
    # This defines the other side of the relationship.
    # `item.owner` will give you access to the User object.
    owner = relationship("User", back_populates="items")
