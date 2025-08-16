from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime

from ..database import get_session
from ..models import User, Transaction, Currency, TransactionType
from ..schemas import TransactionCreate, TransactionRead, BalanceResponse
from ..dependencies import get_current_user

router = APIRouter()

# Create Transaction
@router.post("/transactions")
def create_transaction(
    transaction: TransactionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if transaction.transaction_type == TransactionType.TRANSFER:
        if not transaction.recipient_id:
            raise HTTPException(status_code=400, detail="Recipient ID is required for transfers")
        
        recipient = session.get(User, transaction.recipient_id)
        if not recipient:
            raise HTTPException(status_code=404, detail="Recipient not found")

        # Create a transaction for the sender (negative amount)
        sender_transaction = Transaction(
            amount=-transaction.amount,  # Negative amount for the sender
            currency=transaction.currency,
            transaction_type=TransactionType.TRANSFER,
            recipient_id=transaction.recipient_id,
            user_id=current_user.id
        )
        session.add(sender_transaction)

        # Create a corresponding transaction for the recipient (positive amount)
        recipient_transaction = Transaction(
            amount=transaction.amount,  # Positive amount for the recipient
            currency=transaction.currency,
            transaction_type=TransactionType.DEPOSIT,  # Deposit for the recipient
            recipient_id=None,  # No recipient for the deposit
            user_id=transaction.recipient_id
        )
        session.add(recipient_transaction)
        session.commit()
        session.refresh(sender_transaction)
        return {"transaction_id": sender_transaction.id, "status": "success"}

    else:
        new_transaction = Transaction(
            amount=transaction.amount,
            currency=transaction.currency,
            transaction_type=transaction.transaction_type,
            recipient_id=transaction.recipient_id,
            user_id=current_user.id
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
    return [TransactionRead.model_validate(t) for t in transactions]

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

    currency = transactions[0].currency if transactions else Currency.USD
    return BalanceResponse(user_id=current_user.id, balance=balance, currency=currency)
