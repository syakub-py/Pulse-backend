import pandas as pd

from App.DB.Models.Message import Message
from App.DB.Models.Chat import Chat
from App.DB.Models.User import User
from App.DB.Session import session_scope as session

from App.LoggerConfig import pulse_logger as logger
from typing import Any, Dict, List, Union
from sqlalchemy import select


def getChatMessages(chatId: int) -> Dict[str, Union[List[Dict[str, Any]], int]]:
    try:
        with session() as db_session:
            user_message_query = (
                select(
                    Message.message_id.label('_id'),
                    Message.sender_id.label('senderId'),
                    Message.message.label('text'),
                    Message.created_at.label('createdAt'),
                    User.name.label('user_name'),
                    User.email.label('email'),
                    User.user_id.label('userId')
                )
                .join(User, User.user_id == Message.sender_id)
                .filter(Message.chat_id == chatId)
                .order_by(Message.created_at)
            )
            messages = db_session.execute(user_message_query).fetchall()
            if not messages:
                return {"data": [], "status_code": 200}

            return {
                "data": [{
                    '_id': msg._id,
                    'text': msg.text,
                    'createdAt': msg.createdAt,
                    'user': {
                        '_id': 0,
                        'name': msg.email if hasattr(msg, 'email') else "Pulse AI",
                        'avatar': getattr(msg, 'userAvatar', None)
                    }
                } for msg in messages],
                "status_code": 200
            }
    except Exception as e:
        logger.error("Error getting chat messages: %s", str(e))
        return {"message": f"Couldn't get chat messages: {str(e)}", "status_code": 500}
