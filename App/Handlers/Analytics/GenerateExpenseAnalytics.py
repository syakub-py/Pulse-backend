from App.DB.Models.Property import Property
from App.DB.Session import session_scope as session
from App.DB.Models.Transaction import Transaction
from App.Utils.GenerateRandomRGBA import generate_random_rgba
from App.LoggerConfig import pulse_logger as logger

from typing import Dict, Any
from sqlalchemy import select

def generateExpenseAnalytics(propertyId: int) -> Dict[str, Any]:
    try:
        with session() as db_session:
            property_filter_stmt = select(Property).filter(Property.property_id == propertyId)
            property = db_session.execute(property_filter_stmt).scalars().first()

            if property is None:
                return {"message": f"No property found with ID {propertyId}", "status_code": 404}

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

            return {"data": mapped_expense_data + [
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
            ], "status_code": 200}

    except Exception as e:
        logger.error("There was an error generating expense analytics" + str(e))
        return {"message": "There was an error generating expense analytics" + str(e), "status_code": 500}
