import random
from fastapi import APIRouter

from App.DB.Models.Property import Property
from App.DB.Utils.Session import session_scope as session
from App.DB.Models.PropertyLease import PropertyLease
from App.DB.Models.Lease import Lease
from App.DB.Models.Transaction import Transaction
from sqlalchemy import func, cast, Date
from typing import Union, Dict, Any
from sqlalchemy import select

router = APIRouter()

def generate_random_rgba() -> str:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = round(random.uniform(0.5, 1), 2)
    return f"rgba({r}, {g}, {b}, {a})"

@router.get("/analytics/generateIncomeAnalytics/{propertyId}")
def generateIncomeAnalytics(propertyId: int) -> Union[Dict[str, Any]]:
    try:
        with session() as db_session:
            property_filter_stmt = select(Property).filter(Property.property_id == propertyId)
            property = db_session.execute(property_filter_stmt).scalars().first()

            if property is None:
                return {"message": f"No property found with ID {propertyId}", "status_code": 404}

            lease_filter_stmt = select(PropertyLease, Lease.lease_id == PropertyLease.lease_id).filter(PropertyLease.property_id == propertyId)
            lease = db_session.execute(lease_filter_stmt).scalars().first()

            if lease is None:
                return {"message": f"No lease found with ID {propertyId}", "status_code": 404}

            income_transactions_filter_stmt = (
                select(
                    func.to_char(cast(Transaction.date, Date), 'MM').label('month'),
                    func.sum(Transaction.amount).label('total_amount')
                )
                .filter(Transaction.property_id == propertyId)
                .filter(Transaction.income_or_expense == "income")
                .group_by('month')
                .order_by('month')
            )
            income_transactions = db_session.execute(income_transactions_filter_stmt).fetchall()

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