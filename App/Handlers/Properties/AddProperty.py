from App.DB.Session import session_scope as session
from App.LoggerConfig import pulse_logger as logger
from App.DB.Models.Property import Property
from App.EndpointParams.PropertyDetails import PropertyDetails
from typing import Dict, Any

def addProperty(postgresId:int, firebaseUserId: str, propertyDetails: PropertyDetails) -> Dict[str, Any]:
    logger.info(f"Adding property for user: {firebaseUserId}")
    if not firebaseUserId or not postgresId:
        logger.error("No userId provided")
        return {"message": "No userId provided", "status_code": 500}

    try:
        with session() as db_session:
            new_property = Property(
                owner_id=postgresId,
                firebase_uid=firebaseUserId,
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
            return {"property_id": int(new_property.property_id), "status_code": 200}
    except Exception as e:
        db_session.rollback()
        logger.error(f"Unexpected error: {str(e)}")
        return {"message": str(e), "status_code": 500}
