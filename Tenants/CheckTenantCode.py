from datetime import datetime

from DB.ORM.Models.PendingTenantSignUp import PendingTenantSignUp

from DB.ORM.Utils.Session import session_scope as session
from fastapi import APIRouter

router = APIRouter()

@router.get("/tenant/checkTenantCode/{tenantCode}")
def checkTenantCode(tenantCode:str):
    with session() as db_session:
        result = db_session.query(PendingTenantSignUp).filter(PendingTenantSignUp.code == tenantCode).first()
        if result:
            if result.expires and result.expires >= datetime.date(datetime.now()) and not result.is_code_used:
                return {"isValid": True, "lease_id": result.lease_id}

        return {"isValid": False, "lease_id": 0}
