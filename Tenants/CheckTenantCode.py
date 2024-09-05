from datetime import datetime

from DB.ORM.Models.PendingTenantSignUp import PendingTenantSignUp

from DB.ORM.Utils.Session import session_scope as session
from fastapi import APIRouter
from LoggerConfig import pulse_logger as logger
from typing import Union, Dict, Any
from sqlalchemy import select, update

router = APIRouter()

@router.get("/tenant/checkTenantCode/{tenantCode}")
def checkTenantCode(tenantCode:str) -> Union[Dict[str, Any]]:
    try:
        if not tenantCode:
            return {"message": "no tenant code was provided", "status_code": 500}
        with session() as db_session:
            pending_signup_select = select(PendingTenantSignUp).filter(PendingTenantSignUp.code == tenantCode)
            result = db_session.execute(pending_signup_select).first()

            # Check for invalid conditions first
            if not result or not result[0].expires or result[0].expires < datetime.date(datetime.now()) or result[0].is_code_used:
                return {"isValid": False, "lease_id": 0}

            pending_signup_update = update(PendingTenantSignUp).where(
                PendingTenantSignUp.code == tenantCode
            ).values(is_code_used=True)
            db_session.execute(pending_signup_update)
            db_session.commit()

            return {"isValid": True, "lease_id": result[0].lease_id}
    except Exception as e:
        logger.error(f"Error retrieving properties: {str(e)}")
        return {"message": str(e), "status_code": 500}
