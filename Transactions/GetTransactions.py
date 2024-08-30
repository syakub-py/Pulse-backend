import pandas as pd
from fastapi import APIRouter

from DB.ORM.Models.Transaction import Transaction
from DB.ORM.Utils.Session import session_scope as session

router = APIRouter()


@router.get('/transaction/getTransaction/{propertyId}')
def getTransactions(propertyId: int):
    try:
        with session() as db_session:
            transactions = db_session.query(Transaction).filter(Transaction.property_id == propertyId).all()

            transaction_data = [
                {
                    "date": transaction.created_at,
                    "amount": transaction.amount,
                    "description": transaction.description,
                    "transactionType": transaction.transaction_type,
                    "incomeOrExpense": transaction.income_or_expense
                }
                for transaction in transactions
            ]

            return pd.DataFrame(transaction_data).to_json(orient='records')
    except Exception as e:
        return {"message": str(e), "status_code":500}
