import pandas as pd
from DB.DbConnection import get_postgres_connection

def getChatMessages(chatId: int) -> list[dict]:
    conn = get_postgres_connection()
    if conn is None:
        return []
    try:
        query = """
                SELECT
                    messages.id as _id,
                    messages.role AS user,
                    messages.message AS text,
                    messages.created_at AS createdAt
                FROM
                    chats
                JOIN
                    messages ON chats.chat_id = messages.chat_id
                WHERE
                    chats.chat_id = %s;
                """
        df = pd.read_sql_query(query, conn, params=(chatId,))
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()
