from fastapi import FastAPI
from DB.DbConnection import get_postgres_connection
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
conn = get_postgres_connection()

@app.get("/getProperties")
def home():
    return {"Hello": "World"}

