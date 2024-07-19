import psycopg2
from psycopg2.extensions import connection
from dotenv import load_dotenv
import os


def get_postgres_connection() -> connection:
    load_dotenv()

    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_port = os.getenv('DB_PORT')

    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        print("DB Connection successful")
        return conn
    except Exception as e:
        print(f"An error occurred: {e}")
