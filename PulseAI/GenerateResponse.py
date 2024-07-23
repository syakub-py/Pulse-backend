import os
from typing import Dict, List
import ollama
from dotenv import load_dotenv

load_dotenv()

def generate_response(prompt: str, messages: List[Dict[str, str]]) -> Dict[str, str]:
    messages.append({'role': 'user', 'content': prompt})

    try:
        response = ollama.chat(model=os.getenv("CHAT_MODEL"), messages=messages)
        return {"text": str(response['message']['content'])}
    except Exception as e:
        return {"error": str(e)}
