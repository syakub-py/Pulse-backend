from fastapi import APIRouter

from DB.ORM.Models.Property import Property
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Models.Lease import Lease

router = APIRouter()

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

            return [
                {
                    "name": "Operating Expenses",
                    "expenseAmount": int(property.operating_expenses),
                    "color": "rgba(255, 99, 132, 1)",
                    "legendFontColor": "#7F7F7F",
                    "legendFontSize": 15,
                },
                {
                    "name": "Property Taxes",
                    "expenseAmount": int(property.property_tax),
                    "color": "rgba(54, 162, 235, 1)",
                    "legendFontColor": "#7F7F7F",
                    "legendFontSize": 15,
                },
                {
                    "name": "Mortgage Payment",
                    "expenseAmount": int(property.mortgage_payment),
                    "color": "rgba(75, 192, 192, 1)",
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

            return {
                "labels": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                "datasets": [
                    {
                        "data": [lease.monthly_rent for i in range(12)],
                        "color": lambda opacity=1: f"rgba(255, 255, 255, {opacity})",
                        "strokeWidth": 4
                    }
                ]
            }

    except Exception as e:
        print("Error:", e)
        return {"message": str(e), "status_code": 500}
