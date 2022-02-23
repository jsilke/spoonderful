from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.spoonderful.config import settings

SQLALCHEMY_DATABASE = f"{settings.rdbms}://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # Local keeps it distinct from the existing Session class.
Base = declarative_base()


def get_db():
    """
    Establish a database session for SQL queries and close the session after. Acts as our dependency for DB interactions.
    """
    with SessionLocal() as db:
        yield db
