import os
from typing import Dict
import ollama
from dotenv import load_dotenv
from fastapi import APIRouter
from LoggerConfig import pulse_logger as logger
from PulseAI.GetChatMessages import getChatMessages
from PulseAI.SaveMessagesToDB import saveMessagesToDB

load_dotenv()

router = APIRouter()

@router.get("/generateResponse/{chat_id}/{prompt}", response_model=Dict[str, str])
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

        try:
            saveMessagesToDB(chat_id, prompt, "user")
        except Exception as e:
            logger.error(f"Failed to save user message to DB: {e}")

        try:
            aiResponse = ollama.chat(model=os.getenv("CHAT_MODEL"), messages=messages_list)
            response_content = aiResponse['message']['content']

            try:
                saveMessagesToDB(chat_id, response_content, "assistant")
            except Exception as e:
                logger.error(f"Failed to save AI response to DB: {e}")

            return {"text": response_content}
        except Exception as e:
            logger.error(f"Failed to generate AI response: {e}")
            return {"error": "Failed to generate AI response"}

    except Exception as e:
        logger.error(f"Failed to process chat: {e}")
        return {"error": "Failed to process chat"}
