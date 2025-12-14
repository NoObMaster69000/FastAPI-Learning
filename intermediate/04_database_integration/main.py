# To run this example:
# 1. cd into the `intermediate/04_database_integration` directory.
# 2. Run `uvicorn main:app --reload` in your terminal.
# 3. This will create a `test.db` file in the same directory.

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

# Import everything from the other files in this directory.
from . import crud, models, schemas
from .database import SessionLocal, engine

# This line creates the database tables.
# If the tables already exist, it will not recreate them.
# In a real application, you would use Alembic for migrations.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- Dependency for Database Session ---

def get_db():
    """
    A dependency that provides a database session for each request.
    - It creates a new `SessionLocal` for each request.
    - It uses a `try...finally` block to ensure the session is always closed,
      even if there is an error during the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Path Operations ---

# The API endpoints (path operations) use the `db` dependency to get a
# database session and then call the appropriate CRUD function.

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user.
    - It checks if a user with the same email already exists.
    - If so, it raises an HTTPException.
    - Otherwise, it calls the `create_user` CRUD function.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Reads a list of users with pagination.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Reads a single user by their ID.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    """
    Creates an item for a specific user.
    """
    # You might want to add a check here to ensure the user exists.
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Reads a list of items.
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
