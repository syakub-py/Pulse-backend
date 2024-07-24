from typing import Dict
from fastapi import APIRouter
from DB.ORM.Utils.Session import session
from LoggerConfig import logger
from DB.ORM.Models.Property import Property
from pydantic import BaseModel
router = APIRouter()


class PropertyDetails(BaseModel):
    Name: str
    Address: str
    PropertyType: str

@router.post("/addProperty/{userId}")
def addProperty(userId: str, propertyDetails: PropertyDetails) -> Dict[str, int]:
    logger.info(f"Adding property for user: {userId}")
    if not userId:
        logger.error("No userId provided")
    try:
        new_property = Property(
            user_id=userId,
            nick_name=propertyDetails.Name,
            address=propertyDetails.Address,
            property_type=propertyDetails.PropertyType
        )

        session.add(new_property)
        session.commit()

        logger.info(f"Property added successfully. Property ID: {new_property.property_id}")
        return {"property_id": int(new_property.property_id)}

    except Exception as e:
        session.rollback()
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        session.close()
