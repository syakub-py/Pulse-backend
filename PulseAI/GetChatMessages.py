import pandas as pd
from DB.DbConnection import get_postgres_connection
from typing import Any


def getChatMessages(chatId: int) -> dict[str, Any]:
    conn = get_postgres_connection()
    if conn is None:
        return []

    try:
        query = """
                SELECT
                    messages.id AS message_id,
                    messages.user_id AS message_user_id,
                    messages.role AS message_role,
                    messages.message,
                    messages.created_at AS message_created_at
                FROM
                    chats
                JOIN
                    messages ON chats.chat_id = messages.chat_id
                WHERE
                    chats.chat_id = %s;
                """
        df = pd.read_sql_query(query, conn, params=(chatId,))
        # return [Message(user_id=row['message_user_id'], role=row['message_role'], message=row['message']) for index, row in df.iterrows()]
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

chat_info = getChatMessages(1)
print(chat_info)
