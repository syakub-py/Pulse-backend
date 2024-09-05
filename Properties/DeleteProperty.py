from fastapi import APIRouter
from DB.ORM.Models.Property import Property
from DB.ORM.Models.Lease import Lease
from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Models.TenantLease import TenantLease
from DB.ORM.Models.Todo import Todo
from DB.ORM.Models.Transaction import Transaction
from DB.ORM.Utils.Session import session_scope as session
from LoggerConfig import pulse_logger as logger
from DB.ORM.Models.PendingTenantSignUp import PendingTenantSignUp
from typing import Dict, Any
from sqlalchemy import select

router = APIRouter()

@router.delete("/property/deleteProperty/{propertyId}")
def deleteProperty(propertyId: int) -> Dict[str, Any]:
    try:
        with session() as db_session:
            property_stmt = select(Property).where(Property.property_id == propertyId)
            property_to_delete = db_session.execute(property_stmt).scalars().first()

            if not property_to_delete:
                logger.error(f"Property {propertyId} not found")
                return {"message": "Property not found", "status_code": 500}

            property_leases_stmt = select(PropertyLease).where(PropertyLease.property_id == propertyId)
            property_leases_to_delete = db_session.execute(property_leases_stmt).scalars().all()
            lease_ids = [pl.lease_id for pl in property_leases_to_delete]

            leases_stmt = select(Lease).where(Lease.lease_id.in_(lease_ids))
            leases_to_delete = db_session.execute(leases_stmt).scalars().all()

            tenant_ids = []
            for lease in leases_to_delete:
                tenant_leases_stmt = select(TenantLease).where(TenantLease.lease_id == lease.lease_id)
                tenant_leases = db_session.execute(tenant_leases_stmt).scalars().all()
                tenant_ids.extend([tl.tenant_id for tl in tenant_leases])
                for tenant_lease in tenant_leases:
                    db_session.delete(tenant_lease)

            todos_stmt = select(Todo).where(Todo.property_id == propertyId)
            todos_to_delete = db_session.execute(todos_stmt).scalars().all()

            transactions_stmt = select(Transaction).where(Transaction.property_id == propertyId)
            transactions_to_delete = db_session.execute(transactions_stmt).scalars().all()

            pending_signups_stmt = select(PendingTenantSignUp).where(PendingTenantSignUp.lease_id.in_(lease_ids))
            pending_signups_to_delete = db_session.execute(pending_signups_stmt).scalars().all()

            for signup in pending_signups_to_delete:
                db_session.delete(signup)
            db_session.flush()

            for property_lease in property_leases_to_delete:
                db_session.delete(property_lease)
            db_session.flush()

            for lease in leases_to_delete:
                db_session.delete(lease)
            db_session.flush()

            db_session.delete(property_to_delete)
            db_session.flush()

            for todo in todos_to_delete:
                db_session.delete(todo)
            db_session.flush()

            for transaction in transactions_to_delete:
                db_session.delete(transaction)
            db_session.flush()

            db_session.commit()

            logger.info(f"Deleted Property {propertyId} and associated leases, tenants, todos, and transactions")
            return {"message": "Property and associated data deleted successfully", "status_code": 200}
    except Exception as e:
        logger.error(f"Error deleting property with property ID {propertyId}: " + str(e))
        db_session.rollback()
        return {"message": str(e), "status_code": 500}
