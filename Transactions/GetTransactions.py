import pandas as pd
from fastapi import APIRouter

from DB.ORM.Models.Transaction import Transaction
from DB.ORM.Utils.Session import session_scope as session

router = APIRouter()


@router.get('/transactions/getTransactions/${propertyId}')
def getTransactions(propertyId: int):
    with session() as db_session:
        transactions = db_session.query(Transaction).filter(Transaction.property_id == propertyId).all()

        transaction_data = [
            {
                "amount": transaction.amount,
                "description": transaction.description,
                "transactionType": transaction.transaction_type,
            }
            for transaction in transactions
        ]

        return pd.DataFrame(transaction_data).to_json(orient='records')
