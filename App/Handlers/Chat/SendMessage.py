from fastapi import APIRouter, WebSocket

from App.Utils.Chats.SaveMessageToDB import saveMessageToDB
from App.DB.Models.Message import Message
from App.SocketConnection import isUserActive

router = APIRouter()

@router.post("/chat/sendMessage/")
async def send_message(message: Message, websocket: WebSocket) -> None:
    saveMessageToDB(int(message.chat_id), str(message.message), int(message.sender_id))
    if isUserActive(int(message.sender_id)):
        await websocket.send_text(str(message.message))