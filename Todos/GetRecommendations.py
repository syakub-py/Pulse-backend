from fastapi import APIRouter
import ollama
from dotenv import load_dotenv
import os

router = APIRouter()
load_dotenv()


@router.get("/todo/getRecommendations/{prompt}")
def getRecommendations(prompt: str):
    system_prompt = {"role": "system", "content": """You are an expert assistant specializing in recommending professionals to resolve property management issues. When the user provides a description of a problem, your task is to identify the most appropriate type of professional or service provider to address the issue. Your response should always consist of just the professional's title, without any additional information."""}
    messages_list = [system_prompt, {"role": "user", "content": prompt}]
    aiResponse = ollama.chat(model=os.getenv("CHAT_MODEL"), messages=messages_list)

    return aiResponse['message']['content']


