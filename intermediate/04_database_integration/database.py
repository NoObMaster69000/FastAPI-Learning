# In a real application, this file would contain the database connection setup.
# For this example, we'll use SQLAlchemy with a SQLite in-memory database.
# You'll need to install SQLAlchemy:
# pip install sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The database URL. For a real app, this would be in a config file.
# SQLite is used here for simplicity. The "./test.db" file will be created
# in the same directory.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# `create_engine` is the entry point to the database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # `connect_args` is needed only for SQLite. It's to ensure that the
    # same thread that created the connection is the one that uses it.
    connect_args={"check_same_thread": False}
)

# `SessionLocal` will be the database session class.
# Instances of this class will be the actual database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# `Base` will be the base class for our ORM models.
# All our ORM models will inherit from this class.
Base = declarative_base()
