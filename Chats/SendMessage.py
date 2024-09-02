from fastapi import APIRouter, WebSocket

from Chats.SaveMessagesToDB import saveMessagesToDB
from DB.ORM.Models.Message import Message
from SocketConnection import isUserActive

router = APIRouter()


@router.post("/chat/sendMessage/")
async def send_message(message: Message, websocket: WebSocket):
    saveMessagesToDB(message.chat_id, message.message, message.sender_id)
    if isUserActive(message.sender_id):
        await websocket.send_text(message.message)
