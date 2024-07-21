import pandas as pd
from DB.ORM.Models.Message import Message
from DB.ORM.Models.Chat import Chat
from DB.ORM.Utils.Session import session


def getChatMessages(chatId: int) -> list[dict]:
    if session is None:
        return []
    try:
        # Perform the query using SQLAlchemy ORM
        messages = session.query(
            Message.id.label('_id'),
            Message.role.label('user'),
            Message.message.label('text'),
            Message.created_at.label('createdAt')
        ).join(Chat, Chat.chat_id == Message.chat_id) \
            .filter(Chat.chat_id == chatId) \
            .all()

        df = pd.DataFrame([{
            '_id': msg._id,
            'user': msg.user,
            'text': msg.text,
            'createdAt': msg.createdAt
        } for msg in messages])

        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        session.close()
