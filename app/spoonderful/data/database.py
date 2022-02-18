from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from app.config import settings
import os

# SQLAlchemy database setup boilerplate.
RDBMS = "postgresql"
USERNAME = os.getenv("pg_user")
SERVER = os.getenv("pg_server")
PASSWORD = os.getenv("pg_pass")
DATABASE_NAME = "spoonderful"
SQLALCHEMY_DATABASE = f"{RDBMS}://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE_NAME}"
# SQLALCHEMY_DATABASE = f'{RDBMS}://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Establish a database session for SQL queries and close the session after. Acts as our dependency.
    """
    with SessionLocal() as db:
        yield db
