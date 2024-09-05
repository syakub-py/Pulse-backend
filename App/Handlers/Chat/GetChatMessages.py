import pandas as pd

from App.DB.Models.Message import Message
from App.DB.Models.Chat import Chat
from App.DB.Session import session_scope as session

from LoggerConfig import pulse_logger as logger
from typing import Dict, Any, Hashable
from sqlalchemy import select

def getChatMessages(chatId: int) -> list[Dict[str | Hashable, Any]]:
    try:
        with session() as db_session:
            select_chat_messages_stmt = (
                select(
                    Message.message_id.label('_id'),
                    Message.sender_id.label('senderId'),
                    Message.message.label('text'),
                    Message.created_at.label('createdAt')
                )
                .join(Chat, Chat.chat_id == Message.chat_id)
                .filter(Chat.chat_id == chatId)
            )
            messages = db_session.execute(select_chat_messages_stmt).fetchall()

            return pd.DataFrame([{
                '_id': msg._id,
                'senderId': msg.senderId,
                'text': msg.text,
                'createdAt': msg.createdAt
            } for msg in messages]).to_dict(orient='records')
    except Exception as e:
        logger.error("Error getting chat messages: %s", str(e))
        return pd.DataFrame().to_dict(orient='records')
