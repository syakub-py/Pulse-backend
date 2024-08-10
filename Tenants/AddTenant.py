from DB.ORM.Models.PendingTenantSignUp import PendingTenantSignUp
from DB.ORM.Models.Tenant import Tenant
from DB.ORM.Models.TenantLease import TenantLease
from DB.ORM.Utils.Session import session_scope as session

from typing import Dict

from fastapi import APIRouter

from .Classes.TenantDetails import TenantDetails

from LoggerConfig import pulse_logger as logger

router = APIRouter()


@router.post("/tenant/addTenant/")
def addTenant(tenant: TenantDetails) -> Dict[str, int | str]:
    logger.info(f"finding lease Id with {tenant.Name}")

    try:
        with session() as db_session:
            leaseId = db_session.query(PendingTenantSignUp.lease_id).filter(PendingTenantSignUp.email == tenant.Email).first().lease_id

            new_tenant = Tenant(
                user_id=tenant.UserId,
                name=tenant.Name,
                annual_income=tenant.AnnualIncome,
                phone_number=tenant.PhoneNumber,
                date_of_birth=tenant.DateOfBirth,
                email=tenant.Email,
                document_provided_url=tenant.DocumentProvidedUrl,
                social_security=tenant.SocialSecurity,
            )

            db_session.add(new_tenant)
            db_session.flush()

            new_tenant_lease = TenantLease(
                tenant_id=new_tenant.tenant_id,
                lease_id=leaseId
            )

            db_session.add(new_tenant_lease)
            db_session.commit()

            logger.info(f"Tenant added successfully. Tenant ID: {new_tenant.tenant_id}")
            return {"tenant_id": new_tenant.tenant_id}
    except Exception as e:
        db_session.rollback()
        logger.error(f"Unexpected error adding tenant: {str(e)}")
        return {"error": str(e)}
    finally:
        db_session.close()
