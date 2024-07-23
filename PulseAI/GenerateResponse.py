import os
from typing import Dict, List
import ollama
from dotenv import load_dotenv
from LoggerConfig import logger

load_dotenv()

def generateResponse(prompt: str, messages: List[Dict[str, str]]) -> Dict[str, str]:
    messages.append({'role': 'user', 'content': prompt})
    try:
        response = ollama.chat(model=os.getenv("CHAT_MODEL"), messages=messages)
        return {"text": str(response['message']['content'])}
    except Exception as e:
        logger.error("Error generating a response: " + str(e))
        return {"error": str(e)}
