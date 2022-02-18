from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Direction(Enum):
    """
    Tracks dislikes and likes.
    """

    DISLIKE = 0
    LIKE = 1


class Vote(BaseModel):
    """
    Associates likes/dislikes with recipes.
    """

    recipe_id: int
    direction: Direction


class Recommendation(BaseModel):
    """
    Stores a recommended recipe to present to the user.
    """

    name: str
    image: str
    instructions: str
    time_minutes: int
