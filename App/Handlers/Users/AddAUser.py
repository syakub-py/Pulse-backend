from fastapi import APIRouter
from sqlalchemy import select

from DB.ORM.Models.Property import Property
from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Models.TenantLease import TenantLease
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.User import User
from ..App.Models.UserDetails import UserDetails
from Chats.CreateChat import createChat
from typing import Union, Dict, Any

router = APIRouter()


@router.post("/user/addUser/")
def addAUser(user: UserDetails) -> Union[int, Dict[str, Any]]:
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

            #create the pulse AI chat
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

            return int(new_user.user_id)
    except Exception as e:
        return {"message": str(e), "status_code": 500}
