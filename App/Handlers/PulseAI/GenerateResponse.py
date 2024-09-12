import os
from typing import Dict, Any
import ollama
from dotenv import load_dotenv
from App.LoggerConfig import pulse_logger as logger
from App.Handlers.Chat.GetChatMessages import getChatMessages
from App.Utils.Chats.SaveMessageToDB import saveMessageToDB
from ollama import Message

load_dotenv()

def generateResponse(chat_id: int, prompt: str, sender_id:int) -> Dict[str, Any]:
    try:
        messages = getChatMessages(chat_id)
        if not messages:
            messages_list = [Message(role='user', content=prompt)]
        else:
            content = os.getenv("MODEL_SYSTEM_PROMPT")
            if content is None:
                return {"message": "model system prompt not found", "status_code": 500}
            system_prompt = Message(role="system", content=content)
            saveMessageToDB(chat_id, prompt, sender_id)

            messages_list = [system_prompt] + [
                Message(role=msg['user'], content=msg['text'])
                for msg in messages
                if 'user' in msg and 'text' in msg
            ] + [Message(role='user', content=prompt)]

        model = os.getenv("CHAT_MODEL")
        if model is None:
            return {"message": "model not found", "status_code": 500}

        aiResponse = ollama.chat(model, messages=messages_list)

        response_content: str = aiResponse['message']['content']
        saveMessageToDB(chat_id, response_content, 0)
        return {"data": response_content}
    except Exception as e:
        logger.error(f"Failed to process chat: {e}")
        return {"error": "Failed to process chat"}
