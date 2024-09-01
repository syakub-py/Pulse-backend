from fastapi import APIRouter
from DB.ORM.Utils.Session import session_scope as session
from LoggerConfig import pulse_logger as logger
from DB.ORM.Models.Property import Property
from .Classes.PropertyDetails import PropertyDetails

router = APIRouter()

@router.post("/property/addProperty/{userId}")
def addProperty(userId: str, propertyDetails: PropertyDetails):
    logger.info(f"Adding property for user: {userId}")
    if not userId:
        logger.error("No userId provided")
        return {"message":"no userId provided", "status_code":500}
    try:
        with session() as db_session:
            new_property = Property(
                firebase_uid = userId,
                nick_name=propertyDetails.Name,
                address=propertyDetails.Address,
                property_type=propertyDetails.PropertyType,
                is_rental=propertyDetails.isRental,
                property_tax=propertyDetails.Taxes,
                purchase_price=propertyDetails.PurchasePrice,
                mortgage_payment=propertyDetails.MortgagePayment,
                operating_expenses=propertyDetails.OperatingExpenses,
            )

            db_session.add(new_property)
            db_session.commit()

            logger.info(f"Property added successfully. Property ID: {new_property.property_id}")
            return new_property.property_id
    except Exception as e:
        db_session.rollback()
        logger.error(f"Unexpected error: {str(e)}")
        return {"message":str(e), "status_code":500}
    finally:
        db_session.close()
