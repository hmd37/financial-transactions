from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional
from pydantic import EmailStr, Field
from .models import TransactionType, Currency

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

class TransactionCreate(SQLModel):
    amount: float
    currency: Currency
    transaction_type: TransactionType
    recipient_id: Optional[int] = None

class TransactionRead(SQLModel):
    transaction_id: int = Field(alias="id")
    amount: float
    currency: Currency
    transaction_type: TransactionType
    recipient_id: Optional[int]
    timestamp: datetime

    class Config:
        from_attributes = True
        validate_by_name = True

class BalanceResponse(SQLModel):
    user_id: int
    balance: float
    currency: Currency