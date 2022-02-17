from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from data.schemas import Direction


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
    ORM model for a table to store recommendations voted on by users as id pairs.
    """

    __tablename__ = "likes"

    user_id = Column(
        Integer, ForeignKey("users.id"), ondelete="CASCADE", primary_key=True
    )
    recipe_id = Column(Integer, ondelete="CASCADE", primary_key=True)
    direction = Column(Direction, nullable=False, ondelete="CASCADE")
    # TODO look into the ondelete param.
