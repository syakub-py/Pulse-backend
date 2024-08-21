from fastapi import APIRouter
from DB.ORM.Models.Property import Property
from DB.ORM.Models.Lease import Lease
from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Models.TenantLease import TenantLease
from DB.ORM.Models.User import User
from DB.ORM.Models.Todo import Todo
from DB.ORM.Utils.Session import session_scope as session
from LoggerConfig import pulse_logger as logger


router = APIRouter()

@router.delete("/property/deleteProperty/{propertyId}")
def deleteProperty(propertyId: int):
    try:
        with session() as db_session:
            property_to_delete = db_session.query(Property).filter(Property.property_id == propertyId).first()

            if not property_to_delete:
                logger.error(f"Property {propertyId} not found")
                return {"message": "Property not found", "status_code": 500}

            property_leases_to_delete = db_session.query(PropertyLease).filter(PropertyLease.property_id == propertyId).all()
            lease_ids = [pl.lease_id for pl in property_leases_to_delete]

            leases_to_delete = db_session.query(Lease).filter(Lease.lease_id.in_(lease_ids)).all()

            tenant_ids = []
            for lease in leases_to_delete:
                tenant_leases = db_session.query(TenantLease).filter(TenantLease.lease_id == lease.lease_id).all()
                tenant_ids.extend([tl.tenant_id for tl in tenant_leases])
                for tenant_lease in tenant_leases:
                    db_session.delete(tenant_lease)

            tenants_to_delete = db_session.query(User).filter(User.id.in_(tenant_ids)).all()

            todos_to_delete = db_session.query(Todo).filter(Todo.property_id == propertyId).all()

            for tenant in tenants_to_delete:
                db_session.delete(tenant)

            for lease in leases_to_delete:
                db_session.delete(lease)

            for property_lease in property_leases_to_delete:
                db_session.delete(property_lease)

            db_session.delete(property_to_delete)

            for todo in todos_to_delete:
                db_session.delete(todo)

            db_session.commit()

            logger.info(f"Deleted Property {propertyId} and associated leases and tenants")

    except Exception as e:
        logger.error(f"Error deleting property with property ID {propertyId}: " + str(e))
        db_session.rollback()
        return {"error": str(e)}


