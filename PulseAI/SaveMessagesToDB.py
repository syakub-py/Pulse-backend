from DB.DbConnection import get_postgres_connection
import datetime
def saveMessagesToDB(chatId:int, message: str, role:str):
    conn = get_postgres_connection()
    cursor = conn.cursor()

    try:
        print("Saving messages to database")
        cursor.execute("INSERT INTO messages (chat_id, message, role, created_at) VALUES (%s ,%s ,%s, %s)", (chatId, message, role, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    except Exception as e:
        print(f"Error saving message to database: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
