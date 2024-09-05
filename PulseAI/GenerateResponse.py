import os
from typing import Union, Dict, Any
import ollama
from dotenv import load_dotenv
from fastapi import APIRouter
from LoggerConfig import pulse_logger as logger
from Chats.GetChatMessages import getChatMessages
from Chats.SaveMessageToDB import saveMessageToDB
from ollama import Message

load_dotenv()

router = APIRouter()

@router.get("/pulseChat/generateResponse/{chat_id}/{prompt}", response_model=Dict[str, str])
def generateResponse(chat_id: int, prompt: str) -> Union[Dict[str, str], Dict[str, Any]]:
    try:
        messages = getChatMessages(chat_id)
        if not messages:
            messages_list = [Message(role='user', content=prompt)]
        else:
            content=os.getenv("MODEL_SYSTEM_PROMPT")
            if content is None:
                return {"message": "model system prompt not found", "status_code": 500}
            system_prompt = Message(role="system", content=content)

            messages_list = [system_prompt] + [
                Message(role=msg['user'], content=msg['text'])
                for msg in messages
                if 'user' in msg and 'text' in msg
            ] + [Message(role='user', content=prompt)]

        model = os.getenv("CHAT_MODEL")
        if model is None:
            return {"message": "model not found", "status_code": 500}

        aiResponse = ollama.chat(model, messages=messages_list)

        response_content: Dict[str, str] = aiResponse['message']['content']
        return response_content
    except Exception as e:
        logger.error(f"Failed to process chat: {e}")
        return {"error": "Failed to process chat"}
