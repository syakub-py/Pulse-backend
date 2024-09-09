from App.DB.Models.User import User
from App.DB.Session import session_scope as session
from typing import Dict, Any
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from App.LoggerConfig import pulse_logger as logger

def deleteAUser(user_id: int) -> Dict[str, Any]:
    if not user_id:
        return {"message": "User ID is required", "status_code": 400}

    try:
        with session() as db_session:
            user_delete_stmt = delete(User).where(User.user_id == user_id)
            result = db_session.execute(user_delete_stmt)

            if result.rowcount == 0:
                return {"message": "User not found", "status_code": 404}

            db_session.commit()
            logger.info(f"User {user_id} deleted successfully")
            return {"message": "User deleted successfully", "status_code": 200}

    except SQLAlchemyError as e:
        logger.error(f"Database error deleting user {user_id}: {e}")
        db_session.rollback()
        return {"message": "Database error occurred", "status_code": 500}
    except Exception as e:
        logger.error(f"Unexpected error deleting user {user_id}: {e}")
        db_session.rollback()
        return {"message": "An unexpected error occurred", "status_code": 500}
