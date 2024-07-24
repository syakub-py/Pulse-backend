from DB.ORM.Models.Chat import Chat
from DB.ORM.Utils.Session import session
from LoggerConfig import logger
from fastapi import APIRouter

router = APIRouter()


@router.get("/createChat/{userId}", response_model=dict[str, str])
def createChat(userId: str):
    try:
        existing_chat = session.query(Chat).filter(Chat.user_id == userId).first()
        if existing_chat:
            logger.info(f'Chat already exists for user ID: {userId}')
            return {"chat_id": str(existing_chat.chat_id)}

        new_chat = Chat(user_id=userId)
        session.add(new_chat)
        session.commit()
        logger.info('Successfully created chat with ID: %s' % new_chat.user_id)
        return {"chat_id": str(new_chat.chat_id)}
    except Exception as e:
        session.rollback()
        logger.error("Error creating Chat: " + str(e))
        return None
    finally:
        session.close()
