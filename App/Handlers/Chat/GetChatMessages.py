from App.DB.Models.Message import Message
from App.DB.Models.Chat import Chat
from App.DB.Models.User import User
from App.DB.Session import session_scope as session

from App.LoggerConfig import pulse_logger as logger
from typing import  Any, Hashable
from sqlalchemy import select

def getChatMessages(chatId: int) -> dict[str, list[dict[str, dict[str, str | Any] | Any]] | int] | list[
    dict[Hashable, Any]]:
    try:
        with session() as db_session:
            select_chat_messages_stmt = (
                select(
                    Message.message_id.label('_id'),
                    Message.sender_id.label('senderId'),
                    Message.message.label('text'),
                    Message.created_at.label('createdAt'),
                    User.user_id.label('userId'),
                    User.name.label('userName'),
                    # User.avatar.label('userAvatar')
                )
                .join(Chat, Chat.chat_id == Message.chat_id)
                .join(User, User.user_id == Message.sender_id)
                .filter(Chat.chat_id == chatId)
            )
            messages = db_session.execute(select_chat_messages_stmt).fetchall()

            return {
                "data": [{
                    '_id': msg._id,
                    'text': msg.text,
                    'createdAt': msg.createdAt,
                    'user': {
                        '_id': msg.userId,
                        'name': msg.userName,
                        'avatar': msg.userAvatar
                    }
                } for msg in messages],
                "status_code": 200
            }
    except Exception as e:
        logger.error("Error getting chat messages:", str(e))
        return {"message": "couldn't get chat messages: %s" % str(e), "status_code": 500}
