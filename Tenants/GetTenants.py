from LoggerConfig import pulse_logger as logger

from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Tenant import Tenant
from DB.ORM.Models.TenantLease import TenantLease
from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Models.Lease import Lease
from DB.ORM.Models.Property import Property

from fastapi import APIRouter

import pandas as pd

router = APIRouter()

@router.get("/tenant/getTenants/{userId}")
def getTenants(userId: str):
    try:
        with session() as db_session:
            query = db_session.query(
                Tenant.tenant_id.label('tenant_id'),
                Tenant.name.label('tenant_name'),
                Tenant.annual_income.label('annual_income'),
                Tenant.phone_number.label('phone_number'),
                Tenant.date_of_birth.label('date_of_birth'),
                Tenant.email.label('email'),
                Tenant.social_security.label('social_security'),
                Tenant.document_provided_url.label('document_provided_url'),
                Property.user_id.label('user_id'),
                TenantLease.lease_id.label('lease_id')
            ). \
                join(TenantLease, Tenant.tenant_id == TenantLease.tenant_id). \
                join(Lease, TenantLease.lease_id == Lease.lease_id). \
                join(PropertyLease, PropertyLease.lease_id == Lease.lease_id). \
                join(Property, Property.property_id == PropertyLease.property_id). \
                filter(Property.user_id == userId)

            tenants = query.all()

            tenants_list = [
                {
                    "TenantId": tenant.tenant_id,
                    "Name": tenant.tenant_name,
                    "AnnualIncome": tenant.annual_income,
                    "PhoneNumber": tenant.phone_number,
                    "DateOfBirth": tenant.date_of_birth,
                    "SocialSecurity": tenant.social_security,
                    "DocumentProvidedUrl":tenant.document_provided_url,
                    "Email":tenant.email,
                    "LeaseId": tenant.lease_id
                }
                for tenant in tenants
            ]

            return pd.DataFrame(tenants_list).to_json(orient="records")
    except Exception as e:
        logger.error(f"Error retrieving tenants: {str(e)}")
        return pd.DataFrame().to_json(orient="records")
