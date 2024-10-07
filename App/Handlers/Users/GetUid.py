from App.DB.Models.User import User
from App.DB.Session import session_scope as session
from typing import Dict, Union
from sqlalchemy import select

def getUid(firebaseUid: str) -> Dict[str, Union[str, int]]:
    try:
        with session() as db_session:

            user_select_stmt = select(User).filter(User.firebase_uid == firebaseUid)
            result = db_session.execute(user_select_stmt).scalars().first()

            if result is None:
                return {"message": "User not found", "status_code": 404}
            if firebaseUid:
                return {"user_id": int(result.user_id), "status_code": 200}

            return {"message": "User not authenticated", "status_code": 500}
    except Exception as e:
        return {"message": str(e), "status_code": 500}

