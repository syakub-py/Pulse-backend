from DB.ORM.Models.Tenant import Tenant
from DB.ORM.Models.TenantLease import TenantLease
from DB.ORM.Utils.Session import session_scope as session
from fastapi import APIRouter

from typing import Dict
from .Classes.TenantDetails import TenantDetails

from LoggerConfig import pulse_logger as logger

router = APIRouter()


@router.post("/tenant/addTenant/")
def addTenant(tenant: TenantDetails) -> int | Dict[str, int | str]:
    logger.info(f"Adding tenant: {tenant.Name}")
    with session() as db_session:
        try:
            new_tenant = Tenant(
                user_id=tenant.UserId,
                name=tenant.Name,
                annual_income=tenant.AnnualIncome,
                phone_number=tenant.PhoneNumber,
                date_of_birth=tenant.DateOfBirth,
                email=tenant.Email,
                document_provided_url=tenant.DocumentProvidedUrl,
                social_security=tenant.SocialSecurity,
                document_type=tenant.DocumentType,
            )
            db_session.add(new_tenant)
            db_session.flush()

            new_tenant_lease = TenantLease(
                tenant_id=new_tenant.tenant_id,
                lease_id=tenant.LeaseId
            )
            db_session.add(new_tenant_lease)

            db_session.commit()

            logger.info(f"Tenant added successfully. Tenant ID: {new_tenant.tenant_id}")
            return new_tenant.tenant_id

        except Exception as e:
            db_session.rollback()
            logger.error(f"Error during tenant creation: {str(e)}")
            return {"message": str(e), "status_code": 500}
        finally:
            db_session.close()


