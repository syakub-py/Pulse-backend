from fastapi import APIRouter
from DB.ORM.Models.Transaction import Transaction
from DB.ORM.Utils.Session import session_scope as session

from .Classes.TransactionDetails import TransactionDetails

router = APIRouter()

@router.post('/transaction/addTransaction/')
def addTransaction(transaction:TransactionDetails):
    try:
        with session() as db_session:
            new_transaction = Transaction(
                user_id=transaction.userId,
                amount=transaction.amount,
                description=transaction.description,
                transaction_type=transaction.transactionType,
                property_id=transaction.propertyId,
                income_or_expense=transaction.incomeOrExpense,
                date=transaction.date,
            )
            db_session.add(new_transaction)
            db_session.commit()

            return new_transaction.id
    except Exception as e:
        return {"message": str(e), "status_code": 500}
