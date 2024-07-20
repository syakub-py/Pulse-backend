import os
from typing import Dict
import ollama
from dotenv import load_dotenv

load_dotenv()


def generateResponse(prompt: str) -> Dict[str, str]:
    response = ollama.chat(model=os.getenv("CHAT_MODEL"), messages=[{'role': 'user', 'content': prompt}])

    return {"text": str(response['message']['content'])}
