import random
import os

from dotenv import load_dotenv
from fastapi import APIRouter

from DB.ORM.Utils.Session import session_scope as session

from DB.ORM.Models.PendingTenantSignUp import PendingTenantSignUp

import resend


router = APIRouter()
load_dotenv()

@router.get('/tenant/tenantSignUp/{leaseId}/{tenantEmail}')
def tenantSignUp(leaseId: int, tenantEmail: str):
    with session() as db_session:
        unique_code = str(random.randint(100000, 999999))

        new_sign_up = PendingTenantSignUp(
            lease_id=leaseId,
            email=tenantEmail,
            code=unique_code,
            isCodeUsed=False
        )

        db_session.add(new_sign_up)
        db_session.commit()
        db_session.refresh(new_sign_up)

        resend.api_key = os.getenv('RESEND_API_KEY')
        params: resend.Emails.SendParams = {
            "from": "<onboarding@resend.dev>",
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
