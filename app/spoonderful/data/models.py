from app.spoonderful.data.database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.sql.expression import text
from app.spoonderful.data.schemas import Direction


class User(Base):
    """
    ORM model for a table to store user-specific data.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Vote(Base):
    """
    ORM model for a table to store recommendations voted on by users.
    """

    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    recipe_id = Column(Integer, primary_key=True)
    direction = Column(Enum(Direction), nullable=False)
