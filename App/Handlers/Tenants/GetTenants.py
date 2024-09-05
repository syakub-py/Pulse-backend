import pandas as pd
from sqlalchemy import select
from typing import Dict, Any
from App.LoggerConfig import pulse_logger as logger

from App.DB.Session import session_scope as session
from App.DB.Models.User import User
from App.DB.Models.TenantLease import TenantLease
from App.DB.Models.PropertyLease import PropertyLease
from App.DB.Models.Lease import Lease
from App.DB.Models.Property import Property

def getTenants(userId: int) -> (str | Dict[str, Any]):
    if not userId:
        return {"message": "userId is required", "status_code": 500}
    try:
        with session() as db_session:
            tenant_select = (
                select(
                    User.user_id.label('id'),
                    User.name.label('name'),
                    User.annual_income.label('annual_income'),
                    User.phone_number.label('phone_number'),
                    User.date_of_birth.label('date_of_birth'),
                    User.email.label('email'),
                    User.social_security.label('social_security'),
                    User.document_provided_url.label('document_provided_url'),
                    User.document_type.label('document_type'),
                    Property.firebase_uid.label('user_id'),
                    TenantLease.lease_id.label('lease_id')
                )
                .join(TenantLease, User.user_id == TenantLease.tenant_id)
                .join(Lease, TenantLease.lease_id == Lease.lease_id)
                .join(PropertyLease, PropertyLease.lease_id == Lease.lease_id)
                .join(Property, Property.property_id == PropertyLease.property_id)
                .filter(Property.owner_id == userId)
            )
            tenants = db_session.execute(tenant_select).fetchall()

            tenants_list = [
                {
                    "id": tenant.id,
                    "Name": tenant.name,
                    "AnnualIncome": tenant.annual_income,
                    "PhoneNumber": tenant.phone_number,
                    "DateOfBirth": tenant.date_of_birth,
                    "SocialSecurity": tenant.social_security,
                    "DocumentProvidedUrl":tenant.document_provided_url,
                    "DocumentType": tenant.document_type,
                    "Email": tenant.email,
                    "LeaseId": tenant.lease_id
                }
                for tenant in tenants
            ]

            return pd.DataFrame(tenants_list).to_json(orient="records")
    except Exception as e:
        logger.error(f"Error retrieving tenants: {str(e)}")
        return {"message": str(e), "status_code":500}
