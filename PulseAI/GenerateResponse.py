import os
from datetime import datetime
import ollama
from dotenv import load_dotenv
from typing import List, Dict, Any, Mapping, Iterator
from Models.Message import Message

#messages:List[Message]

load_dotenv()

def generateResponse(prompt: str) -> Message:
    response = ollama.chat(model=os.getenv("CHAT_MODEL"), messages=[{'role':'user', 'content': prompt}])
    return Message(user_id=1, message = response['message']['content'], role=response['message'], created_at=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
