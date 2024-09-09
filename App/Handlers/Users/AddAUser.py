from sqlalchemy import select
from App.DB.Models.Property import Property
from App.DB.Models.PropertyLease import PropertyLease
from App.DB.Models.TenantLease import TenantLease
from App.DB.Session import session_scope as session
from App.DB.Models.User import User
from App.Models.UserDetails import UserDetails
from App.Utils.Chats.CreateChat import createChat
from typing import Dict, Any

def addAUser(user: UserDetails) -> Dict[str, Any]:
    try:
        with session() as db_session:
            new_user = User(
                name=user.Name,
                firebase_uid=user.UserId,
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

            createChat(int(new_user.user_id), 0)

            if user.LeaseId is not None:
                new_tenant_lease = TenantLease(
                    tenant_id=new_user.user_id,
                    lease_id=user.LeaseId
                )
                db_session.add(new_tenant_lease)
                db_session.flush()

                stmt = (
                    select(User.user_id)
                    .join(PropertyLease, PropertyLease.lease_id == user.LeaseId)
                    .join(Property, Property.property_id == PropertyLease.property_id)
                    .join(User, Property.owner_id == User.user_id)
                )

                landlord_id = db_session.execute(stmt).scalars().first()

                if landlord_id is None:
                    return {"message": "cannot find landlord", "status_code": 500}

                createChat(landlord_id, int(new_user.user_id))

            db_session.commit()

            return {"userId": int(new_user.user_id), "message": "success"}
    except Exception as e:
        print(f"Error in addAUser: {str(e)}")
        return {"message": str(e), "status_code": 500}
