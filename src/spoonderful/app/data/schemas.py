from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import enum


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


class Direction(enum):
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
    Stores 5 recommended recipes to present to the user.
    """

    recipe_ids: list[int]
    recipe_images: list
    recipe_instructions: list[str]
    recipe_time: list[int]
