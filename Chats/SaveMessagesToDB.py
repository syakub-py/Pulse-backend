from DB.ORM.Models.Message import Message
from DB.ORM.Utils.Session import session_scope as session
from LoggerConfig import pulse_database_logger as logger
from typing import Union

def saveMessagesToDB(chat_id: int, message: str, senderId: int) -> Union[int, None]:
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