from fastapi import APIRouter
from DB.ORM.Models.Property import Property
from DB.ORM.Models.Lease import Lease
from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Utils.Session import session_scope as session
from LoggerConfig import pulse_logger as logger


router = APIRouter()

@router.delete("/deleteProperty/{propertyId}")
def deleteProperty(propertyId: int):
    try:
        with session() as db_session:
            property_to_delete = db_session.query(Property).filter(Property.property_id == propertyId).first()
            if property_to_delete:
                property_leases_to_delete = db_session.query(PropertyLease).filter(PropertyLease.property_id == propertyId).all()

                lease_ids = [pl.lease_id for pl in property_leases_to_delete]
                leases_to_delete = db_session.query(Lease).filter(Lease.lease_id.in_(lease_ids)).all()
                for lease in leases_to_delete:
                    db_session.delete(lease)

                for property_lease in property_leases_to_delete:
                    db_session.delete(property_lease)

                db_session.delete(property_to_delete)
                db_session.commit()

                logger.info(f"Deleted Property {propertyId} and associated leases")
            else:
                logger.error(f"Property {propertyId} not found")
                return {"error": "Property not found"}
    except Exception as e:
        logger.error(f"Error deleting property with property ID {propertyId}: " + str(e))
        db_session.rollback()
        return {"error": str(e)}

