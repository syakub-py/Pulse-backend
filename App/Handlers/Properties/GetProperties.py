from sqlalchemy import or_
from sqlalchemy.orm import aliased
from App.DB.Models.Lease import Lease
from App.DB.Models.PropertyLease import PropertyLease
from App.DB.Models.User import User
from App.DB.Models.TenantLease import TenantLease
from App.DB.Session import session_scope as session
from App.DB.Models.Property import Property
from App.LoggerConfig import pulse_logger as logger
from typing import Dict, Any, List
from sqlalchemy import select

def getProperties(userId: int) -> Dict[str, Any]:
    if not userId:
        return {"message": "userId is required", "status_code": 400}
    try:
        with session() as db_session:
            TenantAlias = aliased(User)
            TenantLeaseAlias = aliased(TenantLease)

            property_stmt = (
                select(
                    Property.property_id,
                    Property.nick_name,
                    Property.address,
                    Property.property_type,
                    Property.is_rental,
                    Property.property_tax,
                    Property.mortgage_payment,
                    Property.operating_expenses,
                    Property.purchase_price,
                    (TenantAlias.user_id == userId).label("is_tenant")
                )
                .outerjoin(PropertyLease, Property.property_id == PropertyLease.property_id)
                .outerjoin(Lease, PropertyLease.lease_id == Lease.lease_id)
                .outerjoin(TenantLeaseAlias, Lease.lease_id == TenantLeaseAlias.lease_id)
                .outerjoin(TenantAlias, TenantLeaseAlias.tenant_id == TenantAlias.user_id)
                .filter(
                    or_(
                        Property.owner_id == userId,
                        TenantAlias.user_id == userId
                    )
                )
            )

            properties = db_session.execute(property_stmt).fetchall()

            properties_list: List[Dict[str, Any]] = [
                {
                    "id": prop.property_id,
                    "Name": prop.nick_name,
                    "Address": prop.address,
                    "PropertyType": prop.property_type,
                    "PurchasePrice": str(prop.purchase_price),
                    "Taxes": str(prop.property_tax),
                    "MortgagePayment": str(prop.mortgage_payment),
                    "OperatingExpenses": str(prop.operating_expenses),
                    "isRental": prop.is_rental,
                    "isCurrentUserTenant": bool(prop.is_tenant),
                }
                for prop in properties
            ]

            if not properties_list:
                return {"message": "No properties found", "status_code": 404}

            logger.info("Got properties successfully")
            return {"data": properties_list, "status_code": 200}
    except Exception as e:
        logger.error(f"Error retrieving properties: {str(e)}")
        return {"message": str(e), "status_code": 500}
