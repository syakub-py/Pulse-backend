from fastapi import APIRouter
from DB.ORM.Models.User import User
from DB.ORM.Utils.Session import session_scope as session
from typing import Union, Dict, Any

router = APIRouter()

@router.get("/user/getUid/{firebase_uid}/{username}")
def getUid(firebase_uid: str, username: str) -> Union[int, Dict[str, Any]]:
    try:
        with session() as db_session:
            user = db_session.query(User).filter(User.email == username).first()
            if not user:
                return {"message": "User not found", "status_code": 404}
            if firebase_uid:
                return int(user.user_id)
            return {"message": "User not authenticated", "status_code": 500}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
