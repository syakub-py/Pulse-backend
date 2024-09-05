from App.DB.Models.Property import Property
from App.DB.Session import session_scope as session
from App.DB.Models.PropertyLease import PropertyLease
from App.DB.Models.Lease import Lease
from App.DB.Models.Transaction import Transaction
from App.Utils.GenerateRandomRGBA import generate_random_rgba

from typing import Union, Dict, Any
from sqlalchemy import select

def generateExpenseAnalytics(propertyId: int) -> Union[Dict[str, Any], list[dict[str, Any]]]:
    try:
        with session() as db_session:
            property_filter_stmt = select(Property).filter(Property.property_id == propertyId)
            property = db_session.execute(property_filter_stmt).scalars().first()

            if property is None:
                return {"message": f"No property found with ID {propertyId}", "status_code": 404}

            lease_filter_stmt = (
                select(Lease)
                .join(PropertyLease, Lease.lease_id == PropertyLease.lease_id)
                .filter(PropertyLease.property_id == propertyId)
            )
            lease = db_session.execute(lease_filter_stmt).scalars().first()

            if lease is None:
                return {"message": f"No lease found with ID {propertyId}", "status_code": 404}

            transaction_filter_stmt = (
                select(Transaction)
                .filter(Transaction.property_id == propertyId)
                .filter(Transaction.income_or_expense == "expense")
            )
            expense_transactions = db_session.execute(transaction_filter_stmt).scalars().all()

            mapped_expense_data = [
                {
                    "name": transaction.transaction_type,
                    "expenseAmount": int(transaction.amount),
                    "color": generate_random_rgba(),
                    "legendFontColor": "#7F7F7F",
                    "legendFontSize": 15,
                }
                for transaction in expense_transactions
            ]

            return mapped_expense_data + [
                {
                    "name": "Operating Expenses",
                    "expenseAmount": property.operating_expenses,
                    "color": generate_random_rgba(),
                    "legendFontColor": "#7F7F7F",
                    "legendFontSize": 15,
                },
                {
                    "name": "Property Taxes",
                    "expenseAmount": property.property_tax,
                    "color": generate_random_rgba(),
                    "legendFontColor": "#7F7F7F",
                    "legendFontSize": 15,
                },
                {
                    "name": "Mortgage Payment",
                    "expenseAmount": property.mortgage_payment,
                    "color": generate_random_rgba(),
                    "legendFontColor": "#7F7F7F",
                    "legendFontSize": 15,
                },
            ]

    except Exception as e:
        return {"message": str(e), "status_code": 500}
