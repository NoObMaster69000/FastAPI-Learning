# To run this example:
# 1. cd into the `intermediate/03_security_basics` directory.
# 2. Run `uvicorn main:app --reload` in your terminal.
# 3. You'll need to install extra dependencies for this example:
#    pip install "python-jose[cryptography]" "passlib[bcrypt]"

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPBasic,
    HTTPBasicCredentials,
    APIKeyHeader,
    APIKeyQuery,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from typing import Optional, List

# --- Configuration ---

# We'll use a simple in-memory "database" of users for this example.
FAKE_USERS_DB = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1f71wXzE4Y2A..5zB5K.9b.Vb.0e.d3B.d0B.d0B.d0B.", # "password"
        "disabled": False,
        "scopes": ["items:read", "users:read"],
    },
    "jane": {
        "username": "jane",
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "hashed_password": "$2b$12$EixZaYVK1f71wXzE4Y2A..5zB5K.9b.Vb.0e.d3B.d0B.d0B.d0B.", # "password"
        "disabled": False,
        "scopes": ["items:read", "items:write"],
    }
}

# --- JWT and Password Hashing ---

SECRET_KEY = "your-secret-key"  # In production, use a strong, secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# `passlib` context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for password flow
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"items:read": "Read items.", "items:write": "Write items."}
)

# --- Pydantic Models ---

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str
    scopes: List[str] = []

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


# --- Security Helper Functions ---

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    # In a real app, you would add an expiry time.
    # from datetime import timedelta, datetime
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(FAKE_USERS_DB, username=token_data.username)
    if user is None:
        raise credentials_exception

    # Check if the user has the required scopes
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": f"Bearer scope='{security_scopes.scope_str}'"}
            )

    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# --- API Key Security ---
API_KEY = "a-very-secret-api-key"
API_KEY_NAME = "access_token"
api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(
    api_key_query: str = Depends(api_key_query),
    api_key_header: str = Depends(api_key_header),
):
    if api_key_query == API_KEY:
        return api_key_query
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API Key"
    )

# --- HTTP Basic Auth ---
http_basic = HTTPBasic()

def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(http_basic)):
    correct_username = "user"
    correct_password = "password"
    if not (credentials.username == correct_username and credentials.password == correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# --- App and Routes ---
app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(FAKE_USERS_DB, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/items/")
async def read_items(current_user: User = Depends(get_current_user)):
    # This endpoint is protected by OAuth2.
    return [{"item": "Portal Gun", "owner": current_user.username}]

@app.post("/items/")
async def write_items(current_user: User = Depends(get_current_user)):
    # This endpoint is protected by OAuth2.
    if "items:write" not in current_user.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return {"message": "You have write access."}

@app.get("/secure/apikey")
async def secure_endpoint_api_key(api_key: str = Depends(get_api_key)):
    return {"message": "You are authenticated with an API Key."}

@app.get("/secure/basic")
async def secure_endpoint_basic_auth(username: str = Depends(verify_basic_auth)):
    return {"message": f"Hello, {username}! You are authenticated with HTTP Basic Auth."}
