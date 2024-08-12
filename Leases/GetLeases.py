from fastapi import APIRouter

from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Models.Lease import Lease
from DB.ORM.Models.Tenant import Tenant
from DB.ORM.Models.TenantLease import TenantLease
from DB.ORM.Utils.Session import session_scope as session
import pandas as pd

from LoggerConfig import pulse_logger as logger

router = APIRouter()

@router.get("/lease/getLeases/{property_id}")
def getLeases(property_id: int):
    try:
        with session() as db_session:
            leases = (
                db_session.query(Lease, Tenant.user_id)
                .join(PropertyLease, Lease.lease_id == PropertyLease.lease_id)
                .join(TenantLease, Lease.lease_id == TenantLease.lease_id)
                .join(Tenant, TenantLease.tenant_id == Tenant.tenant_id)
                .filter(PropertyLease.property_id == property_id)
                .all()
            )

            lease_data = [
                {
                    "LeaseId": lease.Lease.lease_id,
                    "StartDate": lease.Lease.start_date,
                    "EndDate": lease.Lease.end_date,
                    "MonthlyRent": lease.Lease.monthly_rent,
                    "PropertyId": property_id,
                    "TenantUid": lease.user_id,
                }
                for lease in leases
            ]
            df = pd.DataFrame(lease_data)
            logger.info("Got Leases Successfully")
            return df.to_json(orient="records")
    except Exception as e:
        logger.error("Error retrieving leases: " + str(e))
