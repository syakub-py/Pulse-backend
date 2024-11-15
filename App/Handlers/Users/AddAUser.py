from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError
from App.DB.Models.Property import Property
from App.DB.Models.PropertyLease import PropertyLease
from App.DB.Models.TenantLease import TenantLease
from App.DB.Session import session_scope as session
from App.DB.Models.User import User
from App.EndpointParams.UserDetails import UserDetails
from App.Handlers.Chat.CreateChat import createChat
from typing import Dict, Any
from App.LoggerConfig import pulse_logger as logger

def addAUser(user: UserDetails) -> Dict[str, Any]:
    try:
        with session() as db_session:
            logger.info(f"Adding new user: {user.Name}")
            bot_user = db_session.query(User).filter(User.name == "Pulse AI").first()
            if not bot_user:
                bot_user = User(
                    name="Pulse AI",
                    firebase_uid="Pulse_AI",
                    annual_income=0,
                    phone_number="0",
                    date_of_birth="1994-10-10",
                    email="support@pulseai.com",
                    document_provided_url="",
                    social_security="101-101-1001",
                    document_type="",
                )
                db_session.add(bot_user)
                db_session.flush()

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

            createChat(int(new_user.user_id), int(bot_user.user_id))

            if user.LeaseId is not None:
                new_tenant_lease = TenantLease(
                    tenant_id=new_user.user_id,
                    lease_id=user.LeaseId
                )
                db_session.add(new_tenant_lease)
                db_session.flush()
                OwnerUser = aliased(User)

                stmt = (
                    select(OwnerUser.user_id)
                    .join(PropertyLease, PropertyLease.lease_id == user.LeaseId)
                    .join(Property, Property.property_id == PropertyLease.property_id)
                    .where(Property.owner_id == OwnerUser.user_id)
                )

                result = db_session.execute(stmt)
                landlord_row = result.one_or_none()

                if landlord_row is None:
                    logger.error(f"Cannot find landlord for lease ID: {user.LeaseId}")
                    return {"message": "cant find the landlord for this tenant", "status_code": 404}
                landlord_id = landlord_row[0]
                createChat(int(landlord_id), int(new_user.user_id))

            db_session.commit()
            logger.info(f"User {new_user.user_id} added successfully")
            return {"user_id": int(new_user.user_id), "status_code": 201}

    except SQLAlchemyError as e:
        logger.error(f"Database error in addAUser: {str(e)}")
        db_session.rollback()
        return {"message": "Database error occurred", "status_code": 500}
    except Exception as e:
        logger.error(f"Unexpected error in addAUser: {str(e)}")
        db_session.rollback()
        return {"message": "An unexpected error occurred", "status_code": 400}
