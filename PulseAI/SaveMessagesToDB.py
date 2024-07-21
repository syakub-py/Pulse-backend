from datetime import datetime
from DB.ORM.Models.Message import Message
from DB.ORM.Utils.Session import session

def save_messages_to_db(chat_id: int, message: str, role: str):
    try:
        print("Saving messages to database")

        new_message = Message(
            chat_id=chat_id,
            message=message,
            role=role,
            created_at=datetime.utcnow()  # Use UTC time for consistency
        )

        session.add(new_message)

        session.commit()

    except Exception as e:
        print(f"Error saving message to database: {e}")
        session.rollback()

    finally:
        session.close()
