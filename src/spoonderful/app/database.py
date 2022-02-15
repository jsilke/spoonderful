from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLAlchemy database setup boilerplate.
RDBMS = "postgresql"
USERNAME = os.getenv("pg_user")
SERVER = os.getenv("pg_server")
PASSWORD = os.getenv("pg_pass")
DATABASE_NAME = "spoonderful"
SQLALCHEMY_DATABASE = f"{RDBMS}://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
