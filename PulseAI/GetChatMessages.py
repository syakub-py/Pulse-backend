import pandas as pd
from DB.ORM.Models.Message import Message
from DB.ORM.Models.Chat import Chat
from DB.ORM.Utils.Session import session
from LoggerConfig import logger

def getChatMessages(chatId: int) -> pd.DataFrame:
    try:
        messages = session.query(
            Message.id.label('_id'),
            Message.role.label('user'),
            Message.message.label('text'),
            Message.created_at.label('createdAt')
        ).join(Chat, Chat.chat_id == Message.chat_id) \
            .filter(Chat.chat_id == chatId) \
            .all()

        return pd.DataFrame([{
            '_id': msg._id,
            'user': msg.user,
            'text': msg.text,
            'createdAt': msg.createdAt
        } for msg in messages])
    except Exception as e:
        logger.error("Error getting chat messages: %s", str(e))
        return pd.DataFrame()
    finally:
        session.close()
