# This file contains a simple FastAPI application that we will be testing.
# To run this app:
# 1. cd into the `intermediate/06_testing` directory.
# 2. Run `uvicorn main:app --reload` in your terminal.

from fastapi import FastAPI, Depends, HTTPException, Header

# --- A Simple Dependency ---

async def get_current_user(x_token: str = Header(...)):
    """
    A simple dependency that simulates checking for a valid token.
    In a real app, this would be more complex (e.g., decoding a JWT).
    """
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return {"username": "fakeuser"}

# --- The FastAPI App ---

app = FastAPI()

@app.get("/")
def read_root():
    """ The root endpoint. """
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """ An endpoint with a path parameter and an optional query parameter. """
    return {"item_id": item_id, "q": q}

@app.get("/users/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    """
    A protected endpoint that uses the `get_current_user` dependency.
    """
    return current_user
