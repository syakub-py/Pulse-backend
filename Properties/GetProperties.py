from fastapi import APIRouter
import pandas as pd
from sqlalchemy import or_
from sqlalchemy.orm import aliased

from DB.ORM.Models.Lease import Lease
from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Models.Tenant import Tenant
from DB.ORM.Models.TenantLease import TenantLease
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Property import Property

from LoggerConfig import pulse_logger as logger


router = APIRouter()

@router.get("/property/getProperty/{userId}")
def getProperties(userId: str):
    try:
        with session() as db_session:
            # Alias for tenant to join on the same table multiple times
            TenantAlias = aliased(Tenant)
            TenantLeaseAlias = aliased(TenantLease)

            query = (
                db_session.query(
                    Property.property_id,
                    Property.nick_name,
                    Property.address,
                    Property.property_type,
                    Property.is_rental,
                    (TenantAlias.user_id == userId).label("is_tenant")  # Set is_tenant only if userId is in tenants table
                )
                .outerjoin(PropertyLease, Property.property_id == PropertyLease.property_id)
                .outerjoin(Lease, PropertyLease.lease_id == Lease.lease_id)
                .outerjoin(TenantLeaseAlias, Lease.lease_id == TenantLeaseAlias.lease_id)
                .outerjoin(TenantAlias, TenantLeaseAlias.tenant_id == TenantAlias.tenant_id)
                .filter(
                    or_(
                        Property.user_id == userId,  # Check if userId is the property owner
                        TenantAlias.user_id == userId  # Check if userId is a tenant
                    )
                )
            )

            properties = query.all()

            properties_list = [
                {
                    "PropertyId": prop.property_id,
                    "Name": prop.nick_name,
                    "Address": prop.address,
                    "PropertyType": prop.property_type,
                    "isRental": prop.is_rental,
                    "isTenant": bool(prop.is_tenant),
                }
                for prop in properties
            ]

            properties_df = pd.DataFrame(properties_list)
            logger.info("Got properties successfully")

            return properties_df.to_json(orient="records")
    except Exception as e:
        logger.error(f"Error retrieving properties: {str(e)}")
        return pd.DataFrame().to_json(orient="records")
