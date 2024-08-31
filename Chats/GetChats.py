from fastapi import APIRouter
from DB.ORM.Models.Chat import Chat
from DB.ORM.Utils.Session import session_scope as session

router = APIRouter()


@router.get("chat/getChats/{userId}")
def getChats(userId:str):
    try:
        with session() as db_session:
            chats = db_session.query(Chat.user_id.contains([userId])).all()
            if not chats:
                return {"message": "No chats found", "status_code": 404}

            chat_data = [{
                "id": chat.chat_id,
                "chatName": chat.chat_name,
                "lastMessage": chat.last_message,
            }
                for chat in chats
            ]

            return chat_data

    except Exception as e:
        return {"message":str(e), "status_code":500}
