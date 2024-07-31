from fastapi import APIRouter

from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Models.Lease import Lease
from DB.ORM.Models.Property import Property
from DB.ORM.Utils.Session import session_scope as session
import pandas as pd

from LoggerConfig import logger

router = APIRouter()

@router.get("/getLeases/{property_id}")
def getLeases(property_id: int):
    try:
        with session() as db_session:
            property = db_session.query(Property).filter(Property.property_id == property_id).first()
            if not property:
                return []
            leases = (
                db_session.query(Lease)
                .join(PropertyLease, Lease.lease_id == PropertyLease.lease_id)
                .filter(PropertyLease.property_id == property_id)
                .all()
            )

            lease_data = [
                {
                    "LeaseId": lease.lease_id,
                    "StartDate": lease.start_date,
                    "EndDate": lease.end_date,
                    "MonthlyRent": lease.monthly_rent
                }
                for lease in leases
            ]

            df = pd.DataFrame(lease_data)

            return df.to_json(orient="records")
    except Exception as e:
        logger.error("Error retrieving leases: " + str(e))
