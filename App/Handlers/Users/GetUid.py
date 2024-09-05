from App.DB.Models.User import User
from App.DB.Utils.Session import session_scope as session
from typing import Union, Dict, Any
from sqlalchemy import select

def getUid(firebase_uid: str, username: str) -> Union[int, Dict[str, Any]]:
    try:
        with session() as db_session:
            user_select_stmt = select(User).filter(User.email == username)
            result = db_session.execute(user_select_stmt).scalars().first()
            
            if result is None:
                return {"message": "User not found", "status_code": 404}
            if firebase_uid:
                return int(result.user_id)
            
            return {"message": "User not authenticated", "status_code": 500}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
