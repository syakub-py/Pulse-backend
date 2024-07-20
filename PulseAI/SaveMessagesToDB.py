from typing import List, Dict
from DB.DbConnection import get_postgres_connection

def saveMessagesToDB(userId:int, message: str, role:str):
    conn = get_postgres_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO messages (chat_id, user_id, message, role) VALUES (%s ,%s ,%s, %s)", (chatId, userId, message, role))

        conn.commit()
    except Exception as e:
        print(f"Error saving message to database: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
