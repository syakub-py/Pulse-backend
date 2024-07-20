from DB.DbConnection import get_postgres_connection
import psycopg2

def createChat(userId:str):
    conn = get_postgres_connection()

    try:
        cur = conn.cursor()

        insert_query = """
            INSERT INTO chats (user_id,  created_at)
            VALUES (%s, CURRENT_TIMESTAMP)
            RETURNING chat_id;
            """

        cur.execute(insert_query, (userId,))

        chat_id = cur.fetchone()[0]

        conn.commit()

        cur.close()

        return chat_id

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        if conn is not None:
            conn.rollback()
        return None

    finally:
        if conn is not None:
            conn.close()
