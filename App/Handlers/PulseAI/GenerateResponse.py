import ollama
from dotenv import load_dotenv
from App.LoggerConfig import pulse_logger as logger
from App.Handlers.Chat.GetChatMessages import getChatMessages
from App.Handlers.Chat.SaveMessageToDB import saveMessageToDB
from App.DB.Models.User import User
from App.DB.Session import session_scope as session
from ollama import Message
from typing import Dict, Any
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

def generateResponse(chat_id: int, prompt: str, sender_id: int) -> Dict[str, Any]:
    try:
        messages = getChatMessages(chat_id)
        if not messages:
            messages_list = [Message(role='user', content=prompt)]
        else:
            content = os.getenv("MODEL_SYSTEM_PROMPT")
            if content is None:
                logger.error("MODEL_SYSTEM_PROMPT not found in environment variables.")
                return {"message": "model system prompt not found", "status_code": 500}

            system_prompt = Message(role="system", content=content)
            saveMessageToDB(chat_id, prompt, sender_id)

            messages_list = (
                    [system_prompt] +
                    [Message(role= msg['role'], content=msg['text']) for msg in messages if 'role' in msg and 'text' in msg] +
                    [Message(role='user', content=prompt)]
            )
        model = os.getenv("CHAT_MODEL")
        if model is None:
            logger.error("CHAT_MODEL not found in environment variables.")
            return {"message": "CHAT_MODEL not found in environment variables.", "status_code": 500}

        aiResponse = ollama.chat(model, messages=messages_list)
        response_content: str = aiResponse.get('message', {}).get('content', '') if isinstance(aiResponse.get('message', {}), dict) else ''

        if not response_content:
            logger.error("No content in AI response.")
            return {"message": "No content from AI", "status_code": 500}

        with session() as db_session:
            bot_user = db_session.query(User).filter(User.name == "Pulse AI").first()
            if not bot_user:
                logger.error("Bot user 'Pulse AI' not found in database.")
                return {"message": "Bot user not found", "status_code": 500}

            bot_user_id = int(bot_user.user_id)

        saveMessageToDB(chat_id, response_content, bot_user_id)

        return {"data": response_content}

    except Exception as e:
        logger.error(f"Failed to process chat: {e}", exc_info=True)
        return {"error": "Failed to process chat", "status_code": 500}
