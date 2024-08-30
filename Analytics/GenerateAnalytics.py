import random
from fastapi import APIRouter

from DB.ORM.Models.Property import Property
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Models.Lease import Lease
from DB.ORM.Models.Transaction import Transaction
from sqlalchemy import func, cast, Date

router = APIRouter()

def generate_random_rgba():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = round(random.uniform(0.5, 1), 2)
    return f"rgba({r}, {g}, {b}, {a})"

@router.get("/analytics/generateExpenseAnalytics/{propertyId}")
def generateExpenseAnalytics(propertyId: int):
    try:
        with session() as db_session:
            property = db_session.query(Property).filter(Property.property_id == propertyId).first()
            if property is None:
                return {"message": f"No property found with ID {propertyId}", "status_code": 404}

            lease = db_session.query(Lease).join(PropertyLease, Lease.lease_id == PropertyLease.lease_id).filter(PropertyLease.property_id == propertyId).first()
            if lease is None:
                return {"message": f"No lease found with ID {propertyId}", "status_code": 404}

            expense_transactions = (
                db_session.query(Transaction)
                .filter(Transaction.property_id == propertyId)
                .filter(Transaction.income_or_expense == "expense")
                .all()
            )
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
                    "expenseAmount": int(property.operating_expenses),
                    "color": generate_random_rgba(),
                    "legendFontColor": "#7F7F7F",
                    "legendFontSize": 15,
                },
                {
                    "name": "Property Taxes",
                    "expenseAmount": int(property.property_tax),
                    "color": generate_random_rgba(),
                    "legendFontColor": "#7F7F7F",
                    "legendFontSize": 15,
                },
                {
                    "name": "Mortgage Payment",
                    "expenseAmount": int(property.mortgage_payment),
                    "color": generate_random_rgba(),
                    "legendFontColor": "#7F7F7F",
                    "legendFontSize": 15,
                },
            ]

    except Exception as e:
        return {"message": str(e), "status_code": 500}

@router.get("/analytics/generateIncomeAnalytics/{propertyId}")
def generateIncomeAnalytics(propertyId: int):
    try:
        with session() as db_session:

            property = db_session.query(Property).filter(Property.property_id == propertyId).first()
            if property is None:
                return {"message": f"No property found with ID {propertyId}", "status_code": 404}

            lease = db_session.query(Lease).join(PropertyLease, Lease.lease_id == PropertyLease.lease_id).filter(PropertyLease.property_id == propertyId).first()
            if lease is None:
                return {"message": f"No lease found with ID {propertyId}", "status_code": 404}

            income_transactions = (
                db_session.query(
                    func.to_char(cast(Transaction.date, Date), 'MM').label('month'),
                    func.sum(Transaction.amount).label('total_amount')
                )
                .filter(Transaction.property_id == propertyId)
                .filter(Transaction.income_or_expense == "income")
                .group_by('month')
                .order_by('month')
                .all()
            )
            monthly_data = {str(i).zfill(2): 0 for i in range(1, 13)}

            for transaction in income_transactions:
                month = transaction.month
                total_amount = transaction.total_amount
                monthly_data[month] = total_amount + int(lease.monthly_rent)

            print(monthly_data)
            return {
                "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                "data": [monthly_data[str(i).zfill(2)] for i in range(1, 13)],
                "color": generate_random_rgba(),
            }
    except Exception as e:
        print("Error:", e)
        return {"message": str(e), "status_code": 500}
