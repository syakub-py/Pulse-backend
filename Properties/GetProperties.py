from fastapi import APIRouter
import pandas as pd
from DB.ORM.Utils.Session import session
from DB.ORM.Models.Property import Property

router = APIRouter()

@router.get("/getProperty/{userId}")
def GetProperties(userId: str):
    if session is None:
        return pd.DataFrame()

    properties = session.query(Property).filter(Property.user_id == userId).all()

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
    return properties_df.to_json(orient="records")


