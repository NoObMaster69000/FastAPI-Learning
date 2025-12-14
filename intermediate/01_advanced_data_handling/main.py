# To run this example:
# 1. cd into the `intermediate/01_advanced_data_handling` directory.
# 2. Run `uvicorn main:app --reload` in your terminal.

from fastapi import FastAPI, Body, HTTPException, status
from pydantic import BaseModel, Field, validator, EmailStr
from typing import List, Optional, Union

app = FastAPI()

# --- Complex Pydantic Models ---

class Address(BaseModel):
    """ A simple address model. """
    street: str
    city: str
    zip_code: str

class Company(BaseModel):
    """ A model representing a company. """
    name: str
    address: Address # <-- Nested model

class User(BaseModel):
    """ A user model with a nested Company model. """
    username: str
    email: EmailStr # <-- Pydantic provides types for common patterns like emails.
    company: Company # <-- Another nested model

# --- Custom Validators ---

class Item(BaseModel):
    name: str
    price: float
    # --- Field Customization using Field() ---
    # `Field` can be used to add more constraints and metadata.
    tax: Optional[float] = Field(None, gt=0, description="Tax must be greater than 0")
    tags: List[str] = []

    # A custom validator to ensure the name is not too short.
    @validator('name')
    def name_must_be_long_enough(cls, v):
        if len(v) < 3:
            raise ValueError('Name must be at least 3 characters long')
        return v.title() # You can also transform the data.

    # A validator that works with multiple fields.
    @validator('tax', always=True)
    def tax_must_be_less_than_price(cls, v, values):
        if v is not None and 'price' in values and v >= values['price']:
            raise ValueError('Tax must be less than the price')
        return v

# --- Multiple Response Models ---

# You can define different response models for different status codes.
# This is useful for documenting both successful and error responses.
class SuccessResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    detail: str

@app.post(
    "/items/",
    response_model=Item,
    responses={
        404: {"model": ErrorResponse, "description": "Item not found"},
        400: {"model": ErrorResponse, "description": "Invalid data"},
    }
)
def create_item(item: Item):
    """
    Creates an item.
    - Demonstrates custom validators and multiple response models.
    """
    if item.name == "error":
        # This is just for demonstration purposes.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This is a simulated error."
        )
    return item

# --- Dataclasses and TypedDict ---
# FastAPI also supports `dataclasses` and `TypedDict` as alternatives to Pydantic models.

from dataclasses import dataclass

@dataclass
class DataclassItem:
    name: str
    price: float

@app.post("/dataclass_items/")
def create_dataclass_item(item: DataclassItem):
    """
    An endpoint that uses a dataclass for the request body.
    """
    return item

# --- Dynamic Status Code Selection ---
# You can change the status code of the response dynamically.

from fastapi import Response

@app.get("/items/{item_id}")
def get_item(item_id: int, response: Response):
    """
    Retrieves an item.
    - If the item is not found, it changes the status code to 404.
    """
    if item_id > 100:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "Item not found"}
    return {"item_id": item_id, "name": "A sample item"}
