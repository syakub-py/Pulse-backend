import pandas as pd
from fastapi import APIRouter
from sqlalchemy import select
from datetime import datetime
from typing import Union, Dict, Any


from LoggerConfig import pulse_logger as logger
from DB.ORM.Models.PendingTenantSignUp import PendingTenantSignUp
from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Models.Lease import Lease
from DB.ORM.Models.User import User
from DB.ORM.Models.TenantLease import TenantLease
from DB.ORM.Utils.Session import session_scope as session

router = APIRouter()

@router.get("/lease/getLeases/{property_id}")
def getLeases(property_id: int) -> Union[str, Dict[str, Any]]:
    try:
        with session() as db_session:
            select_leases_stmt = (
                select(Lease, User.firebase_uid)
                .join(PropertyLease, Lease.lease_id == PropertyLease.lease_id)
                .join(TenantLease, Lease.lease_id == TenantLease.lease_id)
                .join(User, TenantLease.tenant_id == User.user_id)
                .filter(PropertyLease.property_id == property_id)
            )

            leases = db_session.execute(select_leases_stmt).fetchall()

            pending_signups_stmt = (
                select(Lease, PendingTenantSignUp)
                .join(PropertyLease, Lease.lease_id == PropertyLease.lease_id)
                .join(PendingTenantSignUp, Lease.lease_id == PendingTenantSignUp.lease_id)
                .filter(PropertyLease.property_id == property_id)
            )

            pending_signups = db_session.execute(pending_signups_stmt).fetchall()

            lease_data = [
                {
                    "LeaseId": lease.lease_id,
                    "StartDate": lease.start_date,
                    "EndDate": lease.end_date,
                    "MonthlyRent": lease.monthly_rent,
                    "PropertyId": property_id,
                    "TenantUid": user_id,
                    "isLeaseExpired": datetime.now() > datetime.strptime(lease.end_date, "%Y-%m-%d")
                }
                for lease, user_id in leases
            ]

            pending_signup_data = [
                {
                    "LeaseId": lease.lease_id,
                    "StartDate": lease.start_date,
                    "EndDate": lease.end_date,
                    "MonthlyRent": lease.monthly_rent,
                    "PropertyId": property_id,
                    "TenantUid": "",
                    "isLeaseExpired": datetime.now() > datetime.strptime(lease.end_date, "%Y-%m-%d"),
                    "isTenantCodeExpired": datetime.now().date() > signup.expires
                }
                for lease, signup in pending_signups
                if not signup.is_code_used
            ]

            df = pd.DataFrame(lease_data + pending_signup_data)
            logger.info("Got Leases Successfully")
            return df.to_json(orient="records")
    except Exception as e:
        logger.error("Error retrieving leases: " + str(e))
        return {"message": "Error retrieving leases: " + str(e), "status_code": 500}

