import os
from typing import Dict
import ollama
from dotenv import load_dotenv
from fastapi import APIRouter
from LoggerConfig import pulse_logger as logger
from Chats.GetChatMessages import getChatMessages
from Chats.SaveMessagesToDB import saveMessagesToDB

load_dotenv()

router = APIRouter()

@router.get("/pulseChat/generateResponse/{chat_id}/{prompt}", response_model=Dict[str, str])
def generateResponse(chat_id: int, prompt: str) -> Dict[str, str]:
    try:
        messages = getChatMessages(chat_id)
        if not messages:
            messages_list = [{'role': 'user', 'content': prompt}]
        else:
            system_prompt = {"role": "system", "content": os.getenv("MODEL_SYSTEM_PROMPT")}
            messages_list = [system_prompt] + [
                {'role': msg['user'], 'content': msg['text']}
                for msg in messages
                if 'user' in msg and 'text' in msg
            ] + [{'role': 'user', 'content': prompt}]
        aiResponse = ollama.chat(model=os.getenv("CHAT_MODEL"), messages=messages_list)
        response_content = aiResponse['message']['content']
        return response_content

    except Exception as e:
        logger.error(f"Failed to process chat: {e}")
        return {"error": "Failed to process chat"}
