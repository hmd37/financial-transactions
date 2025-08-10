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


from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

# Existing user models here...

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    amount: float
    currency: str
    transaction_type: str
    recipient_id: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class TransactionCreate(SQLModel):
    amount: float
    currency: str
    transaction_type: str
    recipient_id: Optional[int] = None

class TransactionRead(SQLModel):
    transaction_id: int
    amount: float
    currency: str
    transaction_type: str
    recipient_id: Optional[int]
    timestamp: datetime

class BalanceResponse(SQLModel):
    user_id: int
    balance: float
    currency: str
