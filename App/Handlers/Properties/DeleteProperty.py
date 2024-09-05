from App.DB.Models.Property import Property
from App.DB.Models.Lease import Lease
from App.DB.Models.PropertyLease import PropertyLease
from App.DB.Models.TenantLease import TenantLease
from App.DB.Models.Todo import Todo
from App.DB.Models.Transaction import Transaction
from App.DB.Utils.Session import session_scope as session
from LoggerConfig import pulse_logger as logger
from App.DB.Models.PendingTenantSignUp import PendingTenantSignUp
from typing import Dict, Any
from sqlalchemy import select, delete

def deleteProperty(propertyId: int) -> Dict[str, Any]:
    try:
        with session() as db_session:
            property_stmt = select(Property).where(Property.property_id == propertyId)
            property_to_delete = db_session.execute(property_stmt).scalars().first()

            if not property_to_delete:
                logger.error(f"Property {propertyId} not found")
                return {"message": "Property not found", "status_code": 500}

            tenant_leases_delete_stmt = (
                delete(TenantLease)
                .where(TenantLease.lease_id.in_(
                    select(PropertyLease.lease_id).where(PropertyLease.property_id == propertyId)
                ))
            )
            db_session.execute(tenant_leases_delete_stmt)

            property_leases_delete_stmt = (
                delete(PropertyLease)
                .where(PropertyLease.property_id == propertyId)
            )
            db_session.execute(property_leases_delete_stmt)

            leases_delete_stmt = (
                delete(Lease)
                .where(Lease.lease_id.in_(
                    select(PropertyLease.lease_id).where(PropertyLease.property_id == propertyId)
                ))
            )
            db_session.execute(leases_delete_stmt)

            todos_delete_stmt = delete(Todo).where(Todo.property_id == propertyId)
            db_session.execute(todos_delete_stmt)

            transactions_delete_stmt = delete(Transaction).where(Transaction.property_id == propertyId)
            db_session.execute(transactions_delete_stmt)

            pending_signups_delete_stmt = (
                delete(PendingTenantSignUp)
                .where(PendingTenantSignUp.lease_id.in_(
                    select(PropertyLease.lease_id).where(PropertyLease.property_id == propertyId)
                ))
            )
            db_session.execute(pending_signups_delete_stmt)

            db_session.delete(property_to_delete)

            db_session.commit()

            logger.info(f"Deleted Property {propertyId} and associated leases, tenants, todos, and transactions")
            return {"message": "Property and associated data deleted successfully", "status_code": 200}
    except Exception as e:
        logger.error(f"Error deleting property with property ID {propertyId}: " + str(e))
        db_session.rollback()
        return {"message": str(e), "status_code": 500}
