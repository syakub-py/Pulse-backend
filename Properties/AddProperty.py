from typing import Dict
from fastapi import APIRouter
from DB.ORM.Utils.Session import session_scope as session
from LoggerConfig import logger
from DB.ORM.Models.Property import Property
from pydantic import BaseModel

router = APIRouter()

class PropertyDetails(BaseModel):
    Name: str
    Address: str
    PropertyType: str
    isRental: bool

@router.post("/addProperty/{userId}")
def addProperty(userId: str, propertyDetails: PropertyDetails) -> Dict[str, int | str]:
    logger.info(f"Adding property for user: {userId}")
    if not userId:
        logger.error("No userId provided")
        return {"error": "No userId provided"}

    try:
        with session() as db_session:
            new_property = Property(
                user_id=userId,
                nick_name=propertyDetails.Name,
                address=propertyDetails.Address,
                property_type=propertyDetails.PropertyType,
                is_rental=propertyDetails.isRental,
            )

            db_session.add(new_property)
            db_session.commit()

            logger.info(f"Property added successfully. Property ID: {new_property.property_id}")
            return {"property_id": new_property.property_id}
    except Exception as e:
        db_session.rollback()
        logger.error(f"Unexpected error: {str(e)}")
        return {"error": str(e)}
    finally:
        db_session.close()
