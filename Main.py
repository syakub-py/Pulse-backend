from fastapi import FastAPI, HTTPException
from DB.DbConnection import get_postgres_connection
from dotenv import load_dotenv
from PulseAI.GenerateResponse import generateResponse
from PulseAI.GetChatMessages import getChatMessages
from Models.Message import Message
from typing import List
from starlette.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()
conn = get_postgres_connection()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/chat/{chat_id}", response_model=List[Message])
def get_chat_messages(chat_id: int):
    messages = getChatMessages(chat_id)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this chat ID")
    return messages

@app.get("/generateResponse/{prompt}", response_model= dict[str, str])
def generate_response(prompt: str):
    messages = generateResponse(prompt)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this chat ID")
    return messages
