from fastapi import APIRouter

from DB.ORM.Models.TenantLease import TenantLease
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.User import User
from .Classes.UserDetails import UserDetails
router = APIRouter()

@router.post("/user/addUser/")
def addAUser(user: UserDetails):
    try:
        with session() as db_session:
            new_user = User(
                name=user.Name,
                uid=user.UserId,
                annual_income=user.AnnualIncome,
                phone_number=user.PhoneNumber,
                date_of_birth=user.DateOfBirth,
                email=user.Email,
                document_provided_url=user.DocumentProvidedUrl,
                social_security=user.SocialSecurity,
                document_type=user.DocumentType,
            )
            db_session.add(new_user)
            db_session.flush()

            if user.LeaseId is not None:
                new_tenant_lease = TenantLease(
                    tenant_id=new_user.id,
                    lease_id=user.LeaseId
                )
                db_session.add(new_tenant_lease)
                db_session.flush()

            db_session.commit()

            return new_user.id
    except Exception as e:
        return {"message": str(e), "status_code": 500}
