from fastapi import APIRouter
import resend
import os
import random
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.PendingTenantSignUp import PendingTenantSignUp
from datetime import datetime, timedelta


router = APIRouter()


@router.get("/api/sendEmail/{LeaseId}/{tenantEmail}")
def sendEmail(tenantEmail: str, LeaseId: int):
    unique_code = str(random.randint(100000, 999999))
    try:
        with session() as db_session:
            new_sign_up = PendingTenantSignUp(
                lease_id=LeaseId,
                email=tenantEmail,
                code=unique_code,
                is_code_used=False,
                expires=datetime.now() + timedelta(hours=24)
            )
        db_session.add(new_sign_up)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        return {"message": str(e), "status_code": 500}

    try:
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
        resend.Emails.send(params)
    except Exception as e:
        db_session.rollback()
        return {"message": str(e), "status_code": 500}

