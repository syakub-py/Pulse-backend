from App.DB.Models.Chat import Chat
from App.DB.Models.ChatParticipant import ChatParticipant
from App.DB.Models.User import User
from App.DB.Session import session_scope as session
from typing import Dict, Any
from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from App.LoggerConfig import pulse_logger as logger

def deleteAUser(userId: int) -> Dict[str, Any]:
    if not userId:
        return {"message": "User ID is required", "status_code": 400}

    try:
        with session() as db_session:
            chat_delete_stmt = (
                delete(Chat)
                .where(Chat.chat_id.in_(
                    select(ChatParticipant.chat_id).where(ChatParticipant.user_id == userId)
                ))
            )

            chat_to_delete = db_session.execute(chat_delete_stmt)
            db_session.flush()

            if chat_to_delete.rowcount == 0:
                return {"message": "No chats to delete", "status_code": 200}

            user_delete_stmt = delete(User).where(User.user_id == userId)
            user_to_delete = db_session.execute(user_delete_stmt)
            db_session.flush()

            if user_to_delete.rowcount == 0:
                return {"message": "User not found", "status_code": 404}

            db_session.commit()
            return {"message": "User deleted successfully", "status_code": 200}

    except SQLAlchemyError as e:
        logger.error(f"Database error deleting user {userId}: {e}")
        db_session.rollback()
        return {"message": "Database error occurred", "status_code": 500}
    except Exception as e:
        logger.error(f"Unexpected error deleting user {userId}: {e}")
        db_session.rollback()
        return {"message": "An unexpected error occurred", "status_code": 500}
