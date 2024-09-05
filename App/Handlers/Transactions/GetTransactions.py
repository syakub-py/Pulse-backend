import pandas as pd

from App.DB.Models.Transaction import Transaction
from App.DB.Session import session_scope as session
from typing import Dict, Any
from sqlalchemy import select

def getTransactions(propertyId: int) -> (str | Dict[str, Any]):
    try:
        with session() as db_session:
            transaction_select_stmt = select(Transaction).filter(Transaction.property_id == propertyId)
            transactions = db_session.execute(transaction_select_stmt).scalars()

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
