from DB.ORM.Models.Chat import Chat
from DB.ORM.Utils.Session import session_scope as session
from LoggerConfig import pulse_logger as logger
from fastapi import APIRouter

router = APIRouter()

@router.get("/chat/createChat/{userId}", response_model=dict[str, str])
def createChat(userId: str):
    try:
        with session() as db_session:
            existing_chat = db_session.query(Chat).filter(Chat.user_id == userId).first()
            if existing_chat:
                logger.info(f'Chat already exists for user ID: {userId}')
                return {"chat_id": str(existing_chat.chat_id)}

            new_chat = Chat(user_id=userId)
            db_session.add(new_chat)
            db_session.flush()
            logger.info(f'Successfully created chat with ID: {new_chat.user_id}')
            return {"chat_id": str(new_chat.chat_id)}
    except Exception as e:
        logger.error(f"Error creating Chat: {str(e)}")
        return None
