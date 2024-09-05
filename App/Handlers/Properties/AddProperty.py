from App.DB.Session import session_scope as session
from LoggerConfig import pulse_logger as logger
from App.DB.Models.Property import Property
from App.Models.PropertyDetails import PropertyDetails
from typing import Union, Dict, Any

def addProperty(userId: str, propertyDetails: PropertyDetails) -> Union[int, Dict[str, Any]]:
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
            return int(new_property.property_id)
    except Exception as e:
        db_session.rollback()
        logger.error(f"Unexpected error: {str(e)}")
        return {"message":str(e), "status_code":500}
    finally:
        db_session.close()
