from typing import Dict

from fastapi import APIRouter

from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Lease import Lease

from .Classes.LeaseDetails import LeaseDetails

from LoggerConfig import pulse_logger as logger

router = APIRouter()


@router.post("/lease/addLease/{propertyId}")
def addLease(propertyId: int, lease: LeaseDetails) -> Dict[str, int | str]:
    logger.info(f"Adding lease for property: {propertyId}")
    if not propertyId:
        logger.error("No propertyId provided")
        raise HTTPException(status_code=400, detail="No propertyId provided")

    try:
        with session() as db_session:
            new_lease = Lease(
                start_date=lease.StartDate,
                end_date=lease.EndDate,
                monthly_rent=lease.MonthlyRent,
                terms=lease.Terms,
                is_expired=lease.isExpired,
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
    finally:
        db_session.close()
