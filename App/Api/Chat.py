from typing import Dict
from fastapi import APIRouter
from App.Handlers.Chat.GetChats import getChats
from App.Handlers.Chat.GetChatMessages import getChatMessages
from typing import Dict, Any, Hashable
from App.SocketConnection import sendMessage
# from App.DB.Models.Message import Message
# from fastapi import WebSocket

chatRoutes = APIRouter(prefix="/chat")

@chatRoutes.get("/getMessages/{chatId}", response_model=Dict)
def get_chat_messages(chatId: int) -> list[Dict[str | Hashable, Any]]:
    return getChatMessages(chatId)

@chatRoutes.get("/getChats/{userId}", response_model=Dict)
def get_chats(userId: int) -> (list[Dict[str, Any]] | Dict[str, Any]):
    return getChats(userId)

@chatRoutes.get("/sendMessage/{user_id}/{message}", response_model=Dict)
async def send_message(user_id: int, message: str):
    return await sendMessage(user_id, message)
