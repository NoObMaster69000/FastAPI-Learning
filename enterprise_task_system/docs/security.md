# Security

The `app/core/security.py` module contains the security-related code for the application. This includes functions for creating and verifying JWT tokens, as well as for hashing and verifying passwords.

## `security.py`

```python
# enterprise_task_system/app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
    subject: str | Any, expires_delta: timedelta | None = None
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

- **`pwd_context`:** An instance of `CryptContext` from the `passlib` library. This is used to hash and verify passwords using the bcrypt algorithm.
- **`ALGORITHM`:** The algorithm to use for creating and verifying JWT tokens.
- **`create_access_token`:** This function creates a new JWT token. It takes a `subject` (which is the user's ID) and an optional `expires_delta` as arguments. If no `expires_delta` is provided, it defaults to the value of `ACCESS_TOKEN_EXPIRE_MINUTES` from the application's settings.
- **`verify_password`:** This function verifies a plain-text password against a hashed password.
- **`get_password_hash`:** This function hashes a plain-text password.

## Authentication Flow

The authentication flow in the application is as follows:

1.  The client sends a POST request to the `/api/v1/login/access-token` endpoint with the user's email and password in the request body.
2.  The `login_access_token` endpoint in `app/api/v1/endpoints/login.py` receives the request and calls the `authenticate` method on the `UserRepository` to verify the user's credentials.
3.  If the credentials are valid, the `create_access_token` function is called to create a new JWT token.
4.  The token is returned to the client in the response.
5.  The client then includes the token in the `Authorization` header of all subsequent requests to protected endpoints.
6.  The `get_current_user` dependency in `app/api/deps.py` decodes and validates the token, and then gets the user from the database.
7.  If the token is valid, the user is injected into the endpoint function. If not, an `HTTPException` is raised.
