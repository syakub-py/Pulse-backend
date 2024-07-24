from DB.ORM.Models.Message import Message
from DB.ORM.Utils.Session import session
from LoggerConfig import logger


def saveMessagesToDB(chat_id: int, message: str, role: str):
    try:
        new_message = Message(
            chat_id=chat_id,
            message=message,
            role=role)

        session.add(new_message)
        session.commit()
        logger.info("Saved message to Chat ID: " + str(chat_id) + " with Message: " + str(message))
    except Exception as e:
        logger.error("Error Saving Messages to DB: " + str(e))
        session.rollback()
    finally:
        session.close()
