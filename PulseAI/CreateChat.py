from DB.ORM.Models.Chat import Chat
from DB.ORM.Utils.Session import session

def createChat(userId:str):
    try:
        new_chat = Chat(user_id=userId)
        session.add(new_chat)
        session.commit()
        return new_chat.chat_id

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return None

    finally:
        if session is not None:
            session.close()

print(createChat("admin"))
