# To run this example:
# 1. cd into the `advanced/03_advanced_security` directory.
# 2. Run `uvicorn main:app --reload` in your terminal.
# 3. For CSRF protection, you would typically use a library like `itsdangerous`
#    or a framework-specific extension.

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

# --- App Setup ---
app = FastAPI()

# --- CORS (Cross-Origin Resource Sharing) Middleware ---
# This middleware allows you to control which origins (domains) are allowed
# to make requests to your API. This is a crucial security feature for web apps.

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000", # Example for a React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # List of allowed origins
    allow_credentials=True, # Allow cookies to be included in requests
    allow_methods=["*"], # Allow all HTTP methods
    allow_headers=["*"], # Allow all headers
)

# --- Security Headers Middleware ---
# This is a custom middleware to add common security headers to every response.
# These headers can help to protect against attacks like clickjacking and XSS.

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# --- CSRF (Cross-Site Request Forgery) Protection (Conceptual) ---
# CSRF protection is complex. A common strategy is to use a "double submit cookie"
# pattern. Here's a conceptual middleware. A real implementation would require
# more robust token generation and handling.

# Add a session middleware (needed for CSRF tokens)
# `pip install itsdangerous` is a good library for signing tokens.
app.add_middleware(SessionMiddleware, secret_key="a-very-secret-key")

@app.middleware("http")
async def csrf_middleware(request: Request, call_next):
    # This is a simplified example.
    if request.method in ("POST", "PUT", "DELETE"):
        csrf_token_header = request.headers.get("x-csrf-token")
        csrf_token_cookie = request.cookies.get("csrf_token")

        if not csrf_token_header or not csrf_token_cookie or csrf_token_header != csrf_token_cookie:
            raise HTTPException(status_code=403, detail="CSRF token mismatch")

    response = await call_next(request)
    return response

# --- Example Endpoints ---

@app.get("/")
def read_root():
    """
    A simple endpoint to test the security headers and CORS.
    - Try making a request from a different origin (e.g., a simple HTML file
      opened from your local file system) to see CORS in action.
    """
    return {"message": "Hello with security headers!"}

@app.get("/get-csrf-token")
def get_csrf_token(request: Request):
    """
    An endpoint to get a CSRF token. In a real app, this would be part
    of your login or page load process.
    """
    # A real implementation would use a secure random token.
    token = "a-sample-csrf-token"
    response = JSONResponse({"csrf_token": token})
    response.set_cookie(key="csrf_token", value=token, httponly=True)
    return response

@app.post("/protected-form")
def protected_form():
    """
    A conceptual endpoint that would be protected by the CSRF middleware.
    - You would need to include the `X-CSRF-Token` header and the `csrf_token`
      cookie in your request.
    """
    return {"message": "Your form was successfully submitted."}
