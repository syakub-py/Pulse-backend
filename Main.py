from fastapi import FastAPI, HTTPException
from DB.DbConnection import get_postgres_connection
from dotenv import load_dotenv
from PulseAI.GenerateResponse import generateResponse
from PulseAI.GetChatMessages import getChatMessages
from PulseAI.SaveMessagesToDB import saveMessagesToDB
from PulseAI.CreateChat import createChat
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

@app.get("/chat/{chat_id}")
def get_chat_messages(chat_id: int):
    messages = getChatMessages(chat_id)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this chat ID")
    return messages

@app.get("/generateResponse/{prompt}", response_model= dict[str, str])
def generate_response(prompt: str):
    saveMessagesToDB("", prompt, "user")
    aiResponse = generateResponse(prompt)
    if not aiResponse:
        raise HTTPException(status_code=404, detail="No messages found for this chat ID")

    saveMessagesToDB("", aiResponse['text'], "assistant")
    return aiResponse

@app.get("/createChat/{user_id}", response_model= dict[str, str])
def create_chat(user_id: str):
    chat_id = createChat(user_id)
    print(chat_id)
    return {"chat_id": str(chat_id)}
