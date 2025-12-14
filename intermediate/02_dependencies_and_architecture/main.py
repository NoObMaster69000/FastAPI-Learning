# To run this example:
# 1. cd into the `intermediate/02_dependencies_and_architecture` directory.
# 2. Run `uvicorn main:app --reload` in your terminal.

from fastapi import FastAPI, Depends, Header, HTTPException, status, Cookie
from typing import Optional

# --- Dependency Injection ---

# A dependency is just a function (or a callable) that can take all the same
# parameters that a path operation function can take.

# A simple dependency to get common parameters.
def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    """
    A dependency that provides common query parameters for pagination.
    This function can be "injected" into other path operation functions.
    """
    return {"q": q, "skip": skip, "limit": limit}

# --- Classes as Dependencies ---

# You can also use a class as a dependency. FastAPI will call the `__call__`
# method of the class instance.
class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

# --- Sub-dependencies ---

# Dependencies can have their own dependencies.

def query_extractor(q: Optional[str] = None):
    """ A sub-dependency to extract the query 'q'. """
    if not q:
        return None
    return q

def query_or_cookie_extractor(
    q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)
):
    """
    A dependency that has a sub-dependency (`query_extractor`).
    It tries to get a query from 'q', or falls back to a cookie.
    """
    if not q:
        return last_query
    return q

# --- Global Dependencies ---

# You can add dependencies to the entire application or to an APIRouter.
# These dependencies will be executed for all path operations.

async def verify_token(x_token: str = Header(...)):
    """ A dependency to verify a token. """
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token header invalid")
    return x_token

async def verify_key(x_key: str = Header(...)):
    """ A dependency to verify a key. """
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Key header invalid")
    return x_key

# We can add global dependencies to the app instance.
# All endpoints in this app will require the `verify_token` and `verify_key` headers.
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


# --- Dependencies in Path Operations ---

@app.get("/items/")
def read_items(commons: dict = Depends(common_parameters)):
    """
    Reads items, using the `common_parameters` dependency.
    - FastAPI will call `common_parameters` and pass the result to `commons`.
    """
    # In a real app, you would use `commons` to query a database.
    return {"message": "Reading items", "params": commons}

@app.get("/users/")
def read_users(commons: CommonQueryParams = Depends(CommonQueryParams)):
    """
    Reads users, using the `CommonQueryParams` class as a dependency.
    - FastAPI will create an instance of `CommonQueryParams` and pass it to `commons`.
    """
    return {"message": "Reading users", "params": commons}

@app.get("/search/")
def search(query: str = Depends(query_or_cookie_extractor)):
    """
    A search endpoint that uses a dependency with a sub-dependency.
    - It demonstrates how dependencies can be chained.
    """
    if not query:
        return {"message": "No query found."}
    return {"message": f"Searching for: {query}"}

# This endpoint will have the global dependencies, `verify_token` and `verify_key`,
# applied automatically.
@app.get("/protected-route/")
def protected_route():
    """
    This endpoint is protected by the global dependencies.
    You must provide valid `X-Token` and `X-Key` headers to access it.
    """
    return {"message": "You have access to the protected route."}

# You can also add dependencies to a specific path operation, even if there
# are global dependencies.
@app.get("/items/{item_id}", dependencies=[Depends(verify_token)])
def read_item(item_id: int):
    """
    This endpoint is protected by both the global `verify_key` dependency
    and the path-specific `verify_token` dependency.
    """
    return {"item_id": item_id}
