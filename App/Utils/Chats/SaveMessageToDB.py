from typing import Any, Dict
from App.LoggerConfig import pulse_database_logger as logger
from App.DB.Models.Message import Message
from App.DB.Session import session_scope as session
from App.DB.Models.Chat import Chat

def saveMessageToDB(chat_id: int, message: str, senderId: int) -> Dict[str, Any]:
    try:
        with session() as db_session:
            current_chat = db_session.query(Chat).filter_by(chat_id=chat_id).one()
            new_message = Message(
                chat_id=chat_id,
                message=message,
                sender_id=senderId,
            )

            db_session.add(new_message)
            db_session.flush()

            current_chat.last_message = message
            current_chat.last_message_sender_id = senderId

            db_session.commit()

            return {"message_id": int(new_message.message_id), "status_code": 200}
    except Exception as e:
        logger.error(f"Error Saving Messages to DB: {str(e)}")
        return {"message": f"Error Saving Messages to DB: {str(e)}", "status_code": 500}
