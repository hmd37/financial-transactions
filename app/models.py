from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from pydantic import EmailStr


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: EmailStr
    password: str  # hashed
    created_at: datetime = Field(default_factory=datetime.now)

class UserCreate(SQLModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(SQLModel):
    email: EmailStr
    password: str

class UserProfile(SQLModel):
    user_id: int
    username: str
    email: EmailStr
    created_at: datetime
