from DB.ORM.Models.Chat import Chat
from DB.ORM.Utils.Session import session
from LoggerConfig import logger

def createChat(userId:str):
    try:
        new_chat = Chat(user_id=userId)
        session.add(new_chat)
        session.commit()
        logger.info('Successfully created chat with ID: %s' % new_chat.user_id)
        return new_chat.chat_id
    except Exception as e:
        session.rollback()
        logger.error("Error creating Chat: " + str(e))
        return None
    finally:
        session.close()

