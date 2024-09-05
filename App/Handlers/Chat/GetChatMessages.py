from typing import List
import pandas as pd
from fastapi import APIRouter

from DB.ORM.Models.Message import Message
from DB.ORM.Models.Chat import Chat
from DB.ORM.Utils.Session import session_scope as session

from LoggerConfig import pulse_logger as logger
from typing import Dict, Any, Hashable
from sqlalchemy import select

router = APIRouter()

@router.get("/chat/getMessages/{chatId}")
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
