# To run this example:
# 1. cd into the `advanced/02_advanced_architecture` directory.
# 2. Run `uvicorn main:app --reload` in your terminal.

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from .routers import users, items # Import the routers
from .dependencies import get_query_token, get_token_header

# --- Lifespan Events ---
# Lifespan events allow you to run code before the application starts up
# and when it is shutting down. This is useful for initializing resources
# like database connections or machine learning models.

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run before the app starts
    print("Starting up...")
    # You could, for example, connect to a database here.
    yield
    # Code to run when the app is shutting down
    print("Shutting down...")
    # You could, for example, disconnect from the database here.

app = FastAPI(lifespan=lifespan)

# --- APIRouter ---
# `APIRouter` allows you to organize your path operations into different
# modules or "routers". This helps to keep your code clean and maintainable,
# especially in large applications.

# --- Global Dependencies ---
# You can add dependencies to the entire application or to a specific router.
app.include_router(
    users.router,
    prefix="/users", # All routes in `users.router` will have this prefix.
    tags=["users"], # This will group the routes in the API docs.
    dependencies=[Depends(get_token_header)], # This dependency applies to all routes in this router.
    responses={404: {"description": "Not found"}},
)

app.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
)

# --- Sub-applications ---
# You can also "mount" another FastAPI application as a sub-application.
# This is useful for creating microservices or for composing applications.

sub_app = FastAPI()

@sub_app.get("/sub")
def read_sub():
    return {"message": "Hello from the sub-application"}

app.mount("/subapi", sub_app)

# --- Root Endpoint ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the advanced architecture example."}
