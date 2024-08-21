from datetime import datetime

from DB.ORM.Models.PendingTenantSignUp import PendingTenantSignUp

from DB.ORM.Utils.Session import session_scope as session
from fastapi import APIRouter
from LoggerConfig import pulse_logger as logger

router = APIRouter()

@router.get("/tenant/checkTenantCode/{tenantCode}")
def checkTenantCode(tenantCode:str):
    try:
        if not tenantCode:
            return {"message": "no tenant code was provided", "status_code": 500}
        with session() as db_session:
            result = db_session.query(PendingTenantSignUp).filter(PendingTenantSignUp.code == tenantCode).first()
            if result:
                if result.expires and result.expires >= datetime.date(datetime.now()) and not result.is_code_used:
                    db_session.query(PendingTenantSignUp).filter(
                        PendingTenantSignUp.code == tenantCode
                    ).update({"is_code_used": True})
                    return {"isValid": True, "lease_id": result.lease_id}

            return {"isValid": False, "lease_id": 0}
    except Exception as e:
        logger.error(f"Error retrieving properties: {str(e)}")
        return {"message": str(e), "status_code": 500}
