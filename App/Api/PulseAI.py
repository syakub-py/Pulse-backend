from typing import Dict, Any
from fastapi import APIRouter
from App.Handlers.PulseAI.GenerateResponse import generateResponse

pulseAIRoutes = APIRouter(prefix="/pulseChat")

@pulseAIRoutes.get("/generateResponse/{chat_id}/{prompt}/{sender_id}", response_model=Dict)
def generate_response(chat_id: int, prompt: str, sender_id:int) -> Dict[str, Any]:
    return generateResponse(chat_id, prompt, sender_id)
