from typing import Dict

from fastapi import APIRouter

from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Lease import Lease

from LoggerConfig import logger

router = APIRouter()


@router.delete("/deleteLease/{leaseId}")
def deleteLease(leaseId: int):
    logger.info(f"Deleting lease: {leaseId}")
    if not leaseId:
        logger.error("No leaseId provided")
        return {"error": "No leaseId provided"}

    try:
        with session() as db_session:
            property_lease = db_session.query(PropertyLease).filter(PropertyLease.lease_id == leaseId).first()
            if property_lease:
                db_session.delete(property_lease)
                db_session.commit()

            lease = db_session.query(Lease).filter(Lease.lease_id == leaseId).first()
            if not lease:
                logger.error(f"Lease not found: {leaseId}")
                return {"error": "Lease not found"}

            db_session.delete(lease)
            db_session.commit()

            logger.info(f"Lease deleted successfully: {leaseId}")
    except Exception as e:
        db_session.rollback()
        logger.error(f"Unexpected error deleting a lease: {str(e)}")
        return {"error": str(e)}
    finally:
        db_session.close()
