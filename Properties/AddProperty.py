from typing import Dict
from fastapi import APIRouter
from DB.ORM.Models.Property import Property
from DB.ORM.Utils.Session import session
from LoggerConfig import logger


router = APIRouter()

@router.get("/addProperty/{userId}/{propertyDetails}")
def AddProperty(userId: str, propertyDetails: Dict[str, str]) -> Dict[str, str]:
    logger.info("Adding property for user:", userId)
    if not userId:
        logger.error("No userId provided")
    try:
        new_property = Property(
            user_id=userId,
            address=propertyDetails.get('Address'),
            property_type=propertyDetails.get('PropertyType'),
            image_urls=propertyDetails.get('image_urls'),
            nick_name=propertyDetails.get('Name'),
        )

        session.add(new_property)
        session.commit()

        logger.info(f"Property added successfully. Property ID: {new_property.property_id}")
        return {"property_id": str(new_property.property_id)}

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        session.close()
