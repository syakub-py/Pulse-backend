import resend
import os
import random
from sqlalchemy import func

from App.DB.Models.TenantLease import TenantLease
from App.DB.Models.User import User
from App.DB.Session import session_scope as session
from App.DB.Models.PendingTenantSignUp import PendingTenantSignUp
from datetime import datetime, timedelta
from typing import Dict, Any
from sqlalchemy import select

def sendEmail(tenantEmail: str, LeaseId: int) -> (None | Dict[str, Any]):
    try:
        with session() as db_session:
            user_select_stmt = select(User).filter(func.lower(User.email) == tenantEmail.lower())
            result = db_session.execute(user_select_stmt).scalars().first()

            if result:
                new_tenant_lease = TenantLease(
                    tenant_id=result.user_id,
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

            return {"message":"email sent successfully", "status_code":200}
    except Exception as e:
        db_session.rollback()
        return {"message": str(e), "status_code": 500}


