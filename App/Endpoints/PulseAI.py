from typing import Dict, Any
from fastapi import APIRouter
from App.Handlers.PulseAI.GenerateResponse import generateResponse

pulseAIRoutes = APIRouter(prefix="/pulseChat")

@pulseAIRoutes.get("/generateResponse/{chatId}/{prompt}/{senderId}", response_model=Dict)
def generate_response(chatId: int, prompt: str, senderId: int) -> Dict[str, Any]:
    return generateResponse(chatId, prompt, senderId)
