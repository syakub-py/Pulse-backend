from fastapi import APIRouter

from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Models.Tenant import Tenant
from DB.ORM.Models.TenantLease import TenantLease
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Lease import Lease

from LoggerConfig import pulse_logger as logger

router = APIRouter()


@router.delete("/deleteLease/{leaseId}")
def deleteLease(leaseId: int):
    logger.info(f"Deleting lease: {leaseId}")
    if not leaseId:
        logger.error("No leaseId provided")
        return

    try:
        with session() as db_session:
            tenant_leases = db_session.query(TenantLease).filter(TenantLease.lease_id == leaseId).all()
            tenant_ids = [tenant_lease.tenant_id for tenant_lease in tenant_leases]
            for tenant_lease in tenant_leases:
                db_session.delete(tenant_lease)
            db_session.commit()

            tenants = db_session.query(Tenant).filter(Tenant.tenant_id.in_(tenant_ids)).all()
            for tenant in tenants:
                db_session.delete(tenant)
            db_session.commit()

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

            logger.info(f"Lease and associated tenants deleted successfully: {leaseId}")
    except Exception as e:
        db_session.rollback()
        logger.error(f"Unexpected error deleting a lease: {str(e)}")
        return {"error": str(e)}
    finally:
        db_session.close()
