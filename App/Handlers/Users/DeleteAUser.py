from App.DB.Models.User import User
from App.DB.Session import session_scope as session
from typing import Dict, Any
from sqlalchemy import delete

def deleteAUser(user_id: int) -> Dict[str, Any]:
    try:
        with session() as db_session:
            user_delete_stmt = delete(User).where(User.user_id == user_id)
            result = db_session.execute(user_delete_stmt)

            if result.rowcount == 0:
                return {"message": "User not found", "status_code": 404}

            db_session.commit()
            return {"message": "User deleted successfully", "status_code": 200}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
