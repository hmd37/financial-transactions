from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from ..database import get_session
from ..models import Transaction, TransactionCreate, TransactionRead, BalanceResponse
from ..dependencies import get_current_user
from ..models import User

router = APIRouter()

# Create Transaction
@router.post("/transactions")
def create_transaction(
    transaction: TransactionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    new_transaction = Transaction(
        amount=transaction.amount,
        currency=transaction.currency,
        transaction_type=transaction.transaction_type,
        recipient_id=transaction.recipient_id,
        user_id=current_user.id,
        timestamp=datetime.now()
    )
    session.add(new_transaction)
    session.commit()
    session.refresh(new_transaction)
    return {"transaction_id": new_transaction.id, "status": "success"}

# Get Transaction History
@router.get("/transactions", response_model=list[TransactionRead])
def get_transactions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    transactions = session.exec(
        select(Transaction).where(Transaction.user_id == current_user.id)
    ).all()
    return transactions

# Get User Balance
@router.get("/balance", response_model=BalanceResponse)
def get_balance(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    transactions = session.exec(
        select(Transaction).where(Transaction.user_id == current_user.id)
    ).all()
    balance = sum(t.amount for t in transactions)
    currency = transactions[0].currency if transactions else "USD"
    return BalanceResponse(user_id=current_user.id, balance=balance, currency=currency)
