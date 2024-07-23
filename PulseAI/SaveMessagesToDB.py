from datetime import datetime
from DB.ORM.Models.Message import Message
from DB.ORM.Utils.Session import session

def saveMessagesToDB(chat_id: int, message: str, role: str):
    try:

        new_message = Message(
            chat_id=chat_id,
            message=message,
            role=role,
            created_at=datetime.now().strftime("%a %b %d %Y %H:%M:%S GMT%z")
        )

        session.add(new_message)

        session.commit()

    except Exception as e:
        print(f"Error saving message to database: {e}")
        session.rollback()

    finally:
        session.close()
