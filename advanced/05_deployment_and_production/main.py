# This file demonstrates some best practices for production FastAPI applications.

from fastapi import FastAPI, Request, Depends
from pydantic_settings import BaseSettings
import logging
from logging.config import dictConfig

# --- Configuration Management ---
# Using Pydantic's `BaseSettings`, you can manage your application's
# configuration using environment variables. This is a best practice for
# keeping secrets and settings out of your code.

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    admin_email: str
    database_url: str = "sqlite:///./test.db"

    class Config:
        # This tells Pydantic to look for a .env file.
        # You would create a `.env` file with your settings:
        # ADMIN_EMAIL=admin@example.com
        # DATABASE_URL=postgresql://user:password@host:port/db
        env_file = ".env"

settings = Settings()

# --- Logging ---
# Structured logging is crucial for production applications.
# This example sets up a basic structured logging configuration.
# In a real app, you might use a library like `structlog`.

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s - %(message)s",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)d %(message)s"
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "json": {
            "formatter": "json",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        }
    },
    "loggers": {
        "my-app": {"handlers": ["json"], "level": "INFO"},
    },
}

dictConfig(log_config)
logger = logging.getLogger("my-app")


# --- App and Health Check Endpoints ---
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup.")
    logger.info(f"Admin email: {settings.admin_email}")


@app.get("/health")
def health_check():
    """
    A simple health check endpoint.
    - Monitoring services can use this to check if the application is alive.
    """
    logger.info("Health check endpoint was called.")
    return {"status": "ok"}

@app.get("/config")
def get_config():
    """
    An endpoint to check the loaded configuration (for debugging).
    - Be careful not to expose sensitive information here.
    """
    return {"app_name": settings.app_name, "admin_email": settings.admin_email}
