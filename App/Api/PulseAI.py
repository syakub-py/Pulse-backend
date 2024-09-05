from typing import Dict
from fastapi import APIRouter
from App.Handlers.PulseAI.GenerateResponse import generateResponse

pulseAIRoutes = APIRouter(prefix="/pulseChat")

@pulseAIRoutes.get("/generateResponse/{chat_id}/{prompt}", response_model=Dict)
async def generate_response(chat_id: int, prompt: str):
    return generateResponse(chat_id, prompt)
