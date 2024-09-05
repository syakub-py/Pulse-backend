from fastapi import APIRouter
from DB.ORM.Models.User import User
from DB.ORM.Utils.Session import session_scope as session
from typing import Union, Dict, Any
from sqlalchemy import select

router = APIRouter()

@router.delete('/user/deleteUser/{userId}')
def deleteAUser(userId: int) -> Union[None, Dict[str, Any]]:
    try:
        with session() as db_session:
            user_select_stmt = select(User).filter(User.user_id == userId)
            result = db_session.execute(user_select_stmt).first()

            if result is None:
                return {"message": "User not found", "status_code": 500}

            db_session.delete(result[0])
            db_session.commit()
        return None
    except Exception as e:
        return {"message": str(e), "status_code": 500}
