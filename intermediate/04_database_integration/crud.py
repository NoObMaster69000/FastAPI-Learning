# This file contains the CRUD (Create, Read, Update, Delete) operations
# for your database. This helps to separate the database logic from
# the API logic in your path operations.

from sqlalchemy.orm import Session

from . import models, schemas # Import models and schemas from the same directory.

# --- User CRUD Operations ---

def get_user(db: Session, user_id: int):
    """
    Reads a single user from the database by their ID.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Reads a single user from the database by their email.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Reads a list of users from the database with pagination.
    """
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a new user in the database.
    """
    # In a real app, you would hash the password here.
    # For simplicity, we're storing it in plain text (which is a bad practice).
    fake_hashed_password = user.password + "notreallyhashed"

    # Create a new SQLAlchemy User model instance.
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)

    # Add the new user to the session.
    db.add(db_user)
    # Commit the changes to the database.
    db.commit()
    # Refresh the instance to get the new ID from the database.
    db.refresh(db_user)

    return db_user

# --- Item CRUD Operations ---

def get_items(db: Session, skip: int = 0, limit: int = 100):
    """
    Reads a list of items from the database.
.    """
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    """
    Creates a new item for a specific user.
    """
    # Create a new SQLAlchemy Item model instance.
    db_item = models.Item(**item.dict(), owner_id=user_id)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item
