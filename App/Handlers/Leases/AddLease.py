from App.DB.Models.PropertyLease import PropertyLease
from App.DB.Utils.Session import session_scope as session
from App.DB.Models.Lease import Lease
from fastapi import APIRouter
from typing import Union, Dict, Any

from LoggerConfig import pulse_logger as logger
from Models.LeaseDetails import LeaseDetails

router = APIRouter()


@router.post("/lease/addLease/{propertyId}")
def addLease(propertyId: int, lease: LeaseDetails) -> Union[int, Dict[str, Any]]:
    logger.info(f"Adding lease for property: {propertyId}")

    if not propertyId:
        logger.error("No propertyId provided")
        return {"message": "No propertyId provided", "status_code": 500}

    with session() as db_session:
        try:
            new_lease = Lease(
                start_date=lease.StartDate,
                end_date=lease.EndDate,
                monthly_rent=lease.MonthlyRent,
                terms=lease.Terms,
                is_expired=lease.isLeaseExpired,
            )

            db_session.add(new_lease)
            db_session.flush()

            new_property_lease = PropertyLease(
                property_id=propertyId,
                lease_id=int(new_lease.lease_id)
            )
            db_session.add(new_property_lease)
            db_session.flush()

            db_session.commit()
            logger.info(f"Lease added successfully. Lease ID: {new_lease.lease_id}")
            return int(new_lease.lease_id)
        except Exception as e:
            db_session.rollback()
            logger.error(e)
            if 'unique constraint' in str(e).lower():
                return {"message": "This email was already signed up", "status_code": 409}
            return {"message": str(e), "status_code": 500}
        finally:
            db_session.close()