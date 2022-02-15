from datetime import datetime
from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    password: str


class User(BaseUser):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
