from fastapi import APIRouter, HTTPException, status
from DB.ORM.Models.Property import Property
from DB.ORM.Utils.Session import session
from LoggerConfig import logger

router = APIRouter()

@router.delete("/deleteProperty/{propertyId}")
def deleteProperty(propertyId: int):
    try:
        property_to_delete = session.query(Property).filter(Property.property_id == propertyId).first()
        if property_to_delete:
            session.delete(property_to_delete)
            session.commit()
            logger.info("Deleted Property {}".format(propertyId))
        else:
            logger.error(f"Property {propertyId} not found")
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete property")


