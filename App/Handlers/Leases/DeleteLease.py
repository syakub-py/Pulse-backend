from App.DB.Models.PropertyLease import PropertyLease
from App.DB.Utils.Session import session_scope as session
from App.DB.Models.Lease import Lease
from App.DB.Models.TenantLease import TenantLease
from typing import Union, Dict, Any
from sqlalchemy import delete

from LoggerConfig import pulse_logger as logger

def deleteLease(leaseId: int) -> Union[None, Dict[str, Any]]:
    logger.info(f"Deleting lease: {leaseId}")
    if not leaseId:
        logger.error("No leaseId provided")
        return {"message": "Lease not found", "status_code": 500}

    try:
        with session() as db_session:
            tenant_leases_delete_stmt = delete(TenantLease).where(TenantLease.lease_id == leaseId)
            db_session.execute(tenant_leases_delete_stmt)

            db_session.flush()

            property_lease_delete_stmt = delete(PropertyLease).where(PropertyLease.lease_id == leaseId)
            db_session.execute(property_lease_delete_stmt)

            db_session.flush()

            lease_delete_stmt = delete(Lease).where(Lease.lease_id == leaseId)
            result = db_session.execute(lease_delete_stmt)

            if result.rowcount == 0:
                logger.error(f"Lease not found: {leaseId}")
                return {"message": "Lease not found", "status_code": 500}

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
