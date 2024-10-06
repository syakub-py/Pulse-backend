from fastapi import APIRouter
from App.Handlers.Chat.GetChats import getChats
from App.Handlers.Chat.GetChatMessages import getChatMessages
from typing import Dict, Any, Hashable
from App.EndpointInputModels.MessageDetails import MessageDetails

chatRoutes = APIRouter(prefix="/chat")

@chatRoutes.get("/getMessages/{chatId}", response_model=Dict)
def get_chat_messages(chatId: int) -> list[Dict[str | Hashable, Any]]:
    return getChatMessages(chatId)

@chatRoutes.get("/getChats/{userId}", response_model=Dict)
def get_chats(userId: int) -> (list[Dict[str, Any]] | Dict[str, Any]):
    return getChats(userId)
