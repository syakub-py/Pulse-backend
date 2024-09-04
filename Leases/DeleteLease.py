from fastapi import APIRouter

from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Models.User import User
from DB.ORM.Models.TenantLease import TenantLease
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Lease import Lease
from typing import Union, Dict, Any

from LoggerConfig import pulse_logger as logger

router = APIRouter()


@router.delete("/lease/deleteLease/{leaseId}")
def deleteLease(leaseId: int) -> Union[None, Dict[str, Any]]:
    logger.info(f"Deleting lease: {leaseId}")
    if not leaseId:
        logger.error("No leaseId provided")
        return {"message": "Lease not found", "status_code": 500}

    try:
        with session() as db_session:
            tenant_leases = db_session.query(TenantLease).filter(TenantLease.lease_id == leaseId).all()
            for tenant_lease in tenant_leases:
                db_session.delete(tenant_lease)
            db_session.flush()

            property_lease = db_session.query(PropertyLease).filter(PropertyLease.lease_id == leaseId).first()
            if property_lease:
                db_session.delete(property_lease)
                db_session.flush()

            lease = db_session.query(Lease).filter(Lease.lease_id == leaseId).first()
            if not lease:
                logger.error(f"Lease not found: {leaseId}")
                return {"message": "Lease not found", "status_code": 500}
            db_session.delete(lease)
            db_session.flush()

            db_session.commit()

            logger.info(f"Lease and associated tenants deleted successfully: {leaseId}")
            return None
    except Exception as e:
        db_session.rollback()
        logger.error(f"Unexpected error deleting a lease: {str(e)}")
        return {"message": str(e), "status_code": 500}
    finally:
        db_session.close()
