from fastapi import APIRouter
import resend
import os
import random
from sqlalchemy import func

from DB.ORM.Models.TenantLease import TenantLease
from DB.ORM.Models.User import User
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.PendingTenantSignUp import PendingTenantSignUp
from datetime import datetime, timedelta
from typing import Union, Dict, Any


router = APIRouter()


@router.get("/api/sendEmail/{LeaseId}/{tenantEmail}")
def sendEmail(tenantEmail: str, LeaseId: int) -> Union[Dict[str, Any], None]:
    try:
        with session() as db_session:
            existing_user = db_session.query(User).filter(func.lower(User.email) == tenantEmail.lower()).first()
            if existing_user:
                new_tenant_lease = TenantLease(
                    tenant_id=existing_user.user_id,
                    lease_id=LeaseId
                )
                db_session.add(new_tenant_lease)
                db_session.flush()
            else:
                unique_code = str(random.randint(100000, 999999))
                new_sign_up = PendingTenantSignUp(
                    lease_id=LeaseId,
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
                resend.Emails.send(params)

            db_session.commit()

            return None
    except Exception as e:
        db_session.rollback()
        return {"message": str(e), "status_code": 500}


