from DB.ORM.Models.Message import Message
from DB.ORM.Utils.Session import session_scope as session
from LoggerConfig import pulse_database_logger as logger

def saveMessagesToDB(chat_id: int, message: str, role: str):
    try:
        with session() as db_session:
            new_message = Message(
                chat_id=chat_id,
                message=message,
                role=role)

            db_session.add(new_message)
            db_session.flush()

            return new_message.id
    except Exception as e:
        logger.error(f"Error Saving Messages to DB: {str(e)}")
        return None
