from fastapi import APIRouter

from DB.ORM.Models.Property import Property
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Models.Lease import Lease

router = APIRouter()

@router.get("/analytics/generateAnalytics/{propertyId}")
def generateAnalytics(propertyId: int):
    try:
        with session() as db_session:
            property = db_session.query(Property).filter(Property.property_id == propertyId).first()
            lease = db_session.query(Lease).join(PropertyLease, Lease.lease_id == PropertyLease.lease_id).filter(PropertyLease.property_id == propertyId).first()

            return {
                "monthlyRent": lease.monthly_rent,
                "operatingExpenses": property.operating_expenses,
                "taxes": property.property_tax,
                "totalExpense": (int(property.property_tax)/12) + int(property.operating_expenses) + int(property.mortgage_payment),
            }

    except Exception as e:
        return {"message": str(e), "status_code": 500}
