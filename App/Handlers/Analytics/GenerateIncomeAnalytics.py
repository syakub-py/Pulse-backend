from sqlalchemy import func, cast, Date
from typing import Dict, Any
from sqlalchemy import select
from App.DB.Models.Property import Property
from App.DB.Session import session_scope as session
from App.DB.Models.PropertyLease import PropertyLease
from App.DB.Models.Lease import Lease
from App.DB.Models.Transaction import Transaction
from App.Utils.GenerateRandomRGBA import generate_random_rgba
from App.LoggerConfig import pulse_logger as logger

def generateIncomeAnalytics(propertyId: int) -> Dict[str, Any]:
    try:
        with session() as db_session:
            property_filter_stmt = select(Property).filter(Property.property_id == propertyId)
            property = db_session.execute(property_filter_stmt).scalars().first()

            if property is None:
                return {"message": f"No property found with ID {propertyId}", "status_code": 404}

            lease_filter_stmt = select(PropertyLease, Lease.lease_id == PropertyLease.lease_id).filter(PropertyLease.property_id == propertyId)
            lease = db_session.execute(lease_filter_stmt).scalars().first()

            if lease is None:
                return {"message": f"No lease found with for property with id {propertyId}", "status_code": 404}

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

            return {"data": {
                "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                "data": [monthly_data[str(i).zfill(2)] for i in range(1, 13)],
                "color": generate_random_rgba(),
            }, "status_code": 200}
    except Exception as e:
        logger.error("An error occurred while generating income analytics" + str(e))
        return {"message": "An error occurred while generating income analytics" + str(e), "status_code": 500}
