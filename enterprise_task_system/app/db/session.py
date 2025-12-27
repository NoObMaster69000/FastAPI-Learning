# enterprise_task_system/app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Create the SQLAlchemy engine.
# The engine is the entry point to the database.
# `pool_pre_ping=True` checks connections for liveness before using them.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Create a sessionmaker, which will be a factory for new Session objects.
# `autocommit=False` and `autoflush=False` are the default and recommended
# settings for using SQLAlchemy sessions with FastAPI.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
