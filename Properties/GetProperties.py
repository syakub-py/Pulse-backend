from fastapi import APIRouter
import pandas as pd
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Property import Property

from LoggerConfig import pulse_logger as logger


router = APIRouter()

@router.get("/getProperty/{userId}")
def GetProperties(userId: str):
    try:
        with session() as db_session:
            properties = db_session.query(Property).filter(Property.user_id == userId).all()

            properties_list = [
                {
                    "PropertyId": prop.property_id,
                    "Name": prop.nick_name,
                    "Address": prop.address,
                    "PropertyType": prop.property_type,
                    "isRental": prop.is_rental,
                }
                for prop in properties
            ]

            properties_df = pd.DataFrame(properties_list)
            logger.info("Got properties successfully")

            return properties_df.to_json(orient="records")
    except Exception as e:
        logger.error(f"Error retrieving properties: {str(e)}")
        return pd.DataFrame().to_json(orient="records")
