from DB.ORM.Models.PendingTenantSignUp import PendingTenantSignUp

from DB.ORM.Utils.Session import session_scope as session
from fastapi import APIRouter

router = APIRouter()

@router.get("/tenant/checkTenantCode/{tenantCode}")
def checkTenantCode(tenantCode:str):
    with session() as db_session:
        result = db_session.query(PendingTenantSignUp.lease_id).filter(PendingTenantSignUp.code == int(tenantCode)).first()
        if result:
            return True

        return False
