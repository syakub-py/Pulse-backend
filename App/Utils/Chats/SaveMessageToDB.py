from typing import Union
from App.LoggerConfig import pulse_database_logger as logger
from App.DB.Models.Message import Message
from App.DB.Session import session_scope as session

def saveMessageToDB(chat_id: int, message: str, senderId: int) -> (int | None):
    try:
        with session() as db_session:
            new_message = Message(
                chat_id=chat_id,
                message=message,
                sender_id=senderId
            )

            db_session.add(new_message)
            db_session.flush()

            return int(new_message.message_id)
    except Exception as e:
        logger.error(f"Error Saving Messages to DB: {str(e)}")
        return None
