from typing import Dict
from fastapi import APIRouter
from App.Handlers.Chat.GetChats import getChats
from App.Handlers.Chat.SendMessage import sendMessage
from App.Handlers.Chat.GetChatMessages import getChatMessages

chatRoutes = APIRouter(prefix="/chat")

@chatRoutes.get("/getMessages/{chatId}", response_model=Dict)
async def get_chat_messages(property_id: int):
    return getChatMessages(property_id)

@chatRoutes.get("/getChats/{userId}", response_model=Dict)
async def get_chats(userId: int):
    return getChats(userId)

@chatRoutes.post("/sendMessage/", response_model=Dict)
async def send_message():
    return sendMessage()
