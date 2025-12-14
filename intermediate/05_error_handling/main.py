# To run this example:
# 1. cd into the `intermediate/05_error_handling` directory.
# 2. Run `uvicorn main:app --reload` in your terminal.

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

# --- Custom Exceptions ---

# It's a good practice to create custom exceptions for your application's
# specific errors. This makes the code cleaner and easier to maintain.
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

# --- App and Exception Handlers ---

app = FastAPI()

# --- Custom Exception Handlers ---
# You can add custom exception handlers to catch specific exceptions
# and return a custom response.

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    """
    Handles the custom `UnicornException`.
    - It returns a JSON response with a 418 status code.
    """
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something magical. A unicorn appeared!"},
    )

# --- Overriding the Default Exception Handlers ---

# FastAPI has default exception handlers. You can override them.
# For example, you can override the handler for `RequestValidationError`
# to customize the response for validation errors.

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Customizes the response for Pydantic validation errors.
    - Instead of the default detailed error, this returns a simple message.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Your request has invalid data. Please check the docs."},
    )

# --- Pydantic Model for Validation ---

class Item(BaseModel):
    name: str
    price: float

# --- Path Operations ---

# A simple in-memory "database" for items.
items_db = {"foo": {"name": "Foo", "price": 50.2}, "bar": {"name": "Bar", "price": 62.0}}

@app.get("/items/{item_id}")
def read_item(item_id: str):
    """
    Reads an item.
    - Demonstrates raising `HTTPException` for a "not found" error.
    """
    if item_id not in items_db:
        # --- HTTPException ---
        # `HTTPException` is the standard way to raise HTTP errors in FastAPI.
        # It takes a `status_code` and a `detail` message.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
            # You can also add custom headers.
            headers={"X-Error": "There goes my error"},
        )
    return items_db[item_id]

@app.post("/items/")
def create_item(item: Item):
    """
    Creates an item.
    - This endpoint is used to demonstrate the custom validation error handler.
    - If you send a request with invalid data (e.g., `price` as a string),
      the `validation_exception_handler` will be triggered.
    """
    return item

@app.get("/unicorns/{name}")
def read_unicorn(name: str):
    """
    Demonstrates the custom `UnicornException` handler.
    """

    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
