from typing import Dict

from fastapi import APIRouter

from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Lease import Lease

from .Classes.LeaseDetails import LeaseDetails

from LoggerConfig import pulse_logger as logger

router = APIRouter()


@router.post("/lease/addLease/{propertyId}")
def addLease(propertyId: int, leaseDetails: LeaseDetails) -> Dict[str, int | str]:
    logger.info(f"Adding lease for property: {propertyId}")
    if not propertyId:
        logger.error("No propertyId provided")
        return {"error": "No propertyId provided"}

    try:
        with session() as db_session:
            new_lease = Lease(
                start_date=leaseDetails.StartDate,
                end_date=leaseDetails.EndDate,
                monthly_rent=leaseDetails.MonthlyRent,
            )

            db_session.add(new_lease)
            db_session.flush()

            new_property_lease = PropertyLease(
                property_id=propertyId,
                lease_id=int(new_lease.lease_id)
            )
            db_session.add(new_property_lease)
            db_session.commit()

            logger.info(f"Lease added successfully. Lease ID: {new_lease.lease_id}")
            return {"lease_id": new_lease.lease_id}
    except Exception as e:
        db_session.rollback()
        logger.error(f"Unexpected error adding a lease: {str(e)}")
        return {"error": str(e)}
    finally:
        db_session.close()
