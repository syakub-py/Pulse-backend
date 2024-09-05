from fastapi import APIRouter
from DB.ORM.Models.User import User
from DB.ORM.Utils.Session import session_scope as session
from typing import Union, Dict, Any
from sqlalchemy import delete

router = APIRouter()

@router.delete('/user/deleteUser/{userId}')
def deleteAUser(userId: int) -> Union[None, Dict[str, Any]]:
    try:
        with session() as db_session:
            user_delete_stmt = delete(User).where(User.user_id == userId)
            result = db_session.execute(user_delete_stmt)

            if result.rowcount == 0:
                return {"message": "User not found", "status_code": 500}

            db_session.commit()
        return None
    except Exception as e:
        return {"message": str(e), "status_code": 500}
