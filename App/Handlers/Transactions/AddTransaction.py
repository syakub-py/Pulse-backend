from App.DB.Models.Transaction import Transaction
from App.DB.Session import session_scope as session
from typing import Union, Dict, Any

from App.Models.TransactionDetails import TransactionDetails

def addTransaction(transaction: TransactionDetails) -> Union[int, Dict[str, Any]]:
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

            return int(new_transaction.transaction_id)
    except Exception as e:
        return {"message": str(e), "status_code": 500}
