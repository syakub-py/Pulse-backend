from fastapi import APIRouter, WebSocket

from Chats.SaveMessagesToDB import saveMessagesToDB
from DB.ORM.Models.Message import Message
from SocketConnection import isUserActive

router = APIRouter()


@router.post("/chat/sendMessage/")
async def send_message(message: Message, websocket: WebSocket) -> None:
    saveMessagesToDB(int(message.chat_id), str(message.message), int(message.sender_id))
    if isUserActive(int(message.sender_id)):
        await websocket.send_text(str(message.message))