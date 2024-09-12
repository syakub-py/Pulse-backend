from datetime import datetime
from typing import Any
from App.LoggerConfig import pulse_database_logger as logger
from App.DB.Models.Message import Message
from App.DB.Session import session_scope as session

def saveMessageToDB(chat_id: int, message: str, senderId: int) -> dict[str, Any]:
    try:
        with session() as db_session:
            new_message = Message(
                chat_id=chat_id,
                message=message,
                sender_id=senderId,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            db_session.add(new_message)
            db_session.commit()

            return {"message_id": int(new_message.message_id), "status_code": 200}
    except Exception as e:
        logger.error(f"Error Saving Messages to DB: {str(e)}")
        db_session.rollback()
        return {"message": f"Error Saving Messages to DB: {str(e)}", "status_code": 500}

