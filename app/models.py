from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    transactions: List["Transaction"] = Relationship(back_populates="user")

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    currency: Currency
    transaction_type: TransactionType
    recipient_id: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="transactions")
