import os
from datetime import datetime, timedelta

from psycopg2 import IntegrityError

from DB.ORM.Models.PendingTenantSignUp import PendingTenantSignUp
from DB.ORM.Models.PropertyLease import PropertyLease
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Lease import Lease
from fastapi import APIRouter
import resend
import random
from .Classes.LeaseDetails import LeaseDetails

from LoggerConfig import pulse_logger as logger

router = APIRouter()


@router.post("/lease/addLease/{tenantEmail}/{propertyId}")
def addLease(propertyId: int, tenantEmail:str,lease: LeaseDetails):
    logger.info(f"Adding lease for property: {propertyId}")
    unique_code = str(random.randint(100000, 999999))

    if not propertyId:
        logger.error("No propertyId provided")
        return {"message": "No propertyId provided", "status_code": 500}

    with session() as db_session:
        try:
            new_lease = Lease(
                start_date=lease.StartDate,
                end_date=lease.EndDate,
                monthly_rent=lease.MonthlyRent,
                terms=lease.Terms,
                is_expired=lease.isLeaseExpired,
            )

            db_session.add(new_lease)
            db_session.flush()

            new_property_lease = PropertyLease(
                property_id=propertyId,
                lease_id=int(new_lease.lease_id)
            )
            db_session.add(new_property_lease)
            db_session.flush()

            new_sign_up = PendingTenantSignUp(
                lease_id=new_lease.lease_id,
                email=tenantEmail,
                code=unique_code,
                is_code_used=False,
                expires=datetime.now() + timedelta(hours=24)
            )

            db_session.add(new_sign_up)
            db_session.flush()

            resend.api_key = os.getenv('RESEND_API_KEY')
            params: resend.Emails.SendParams = {
                "from": "Pulse <onboarding@resend.dev>",
                "to": tenantEmail,
                "subject": "Invitation to Join Pulse – Your Tenant Portal",
                "html": """
    <p>You have been invited by your landlord to join Pulse, our property management platform. Please use the following link to sign up:</p>
    
    <p><strong>Sign-Up Link:</strong> <a href="[Insert Link Here]" target="_blank" style="color: #1a73e8;">[Insert Link Here]</a></p>
    
    <p>During the sign-up process, you will need to enter the following code:</p>
    
    <p><strong>Sign-Up Code:</strong> <b>%s</b></p>
    
    <p style="color: #555;">
        <em>Please note that this code will expire in 24 hours.</em>
    </p>""" % unique_code,
            }
            try:
                resend.Emails.send(params)
            except Exception as e:
                db_session.rollback()
                return {"message": str(e), "status_code": 500}

            db_session.commit()
            logger.info(f"Lease added successfully. Lease ID: {new_lease.lease_id}")
            return new_lease.lease_id
        except Exception as e:
            db_session.rollback()
            logger.error(e)
            if 'unique constraint' in str(e).lower():
                return {"message": "This email was already signed up", "status_code": 409}
            return {"message": str(e), "status_code": 500}
        finally:
            db_session.close()
