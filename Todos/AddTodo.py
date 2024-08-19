from datetime import datetime

from fastapi import APIRouter
from LoggerConfig import pulse_logger as logger
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Todo import Todo
import ollama
from dotenv import load_dotenv
import os

from .Classes.TodoDetails import TodoDetails

router = APIRouter()
load_dotenv()

@router.post("/todo/addTodo/")
def addTodo(todo: TodoDetails):
    if not todo:
        return {"message": "no todo details were provided", "status_code": 500}
    try:
        with session() as db_session:
            logger.info("Adding Todo to property id: {}".format(todo.PropertyId))

            system_prompt = {"role": "system", "content": """You are an expert assistant specializing in recommending professionals to resolve property management issues. When the user provides a description of a problem, your task is to identify the most appropriate type of professional or service provider to address the issue. Your response should always consist of just the professional's title, without any additional information."""}
            messages_list = [system_prompt, {"role": "user", "content": todo.Description}]
            aiResponse = ollama.chat(model=os.getenv("CHAT_MODEL"), messages=messages_list)
            professional = aiResponse['message']['content']

            new_todo = Todo(
                property_id=todo.PropertyId,
                title=todo.Title,
                description=todo.Description,
                status=todo.Status,
                priority=todo.Priority,
                added_by=todo.AddedBy,
                recommended_professional=professional,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            db_session.add(new_todo)
            db_session.commit()

            db_session.refresh(new_todo)

            return new_todo.id
    except Exception as e:
        logger.error("Error adding the todo: {}".format(e))
        db_session.rollback()
        return {"message": str(e), "status_code": 500}
    finally:
        db_session.close()






