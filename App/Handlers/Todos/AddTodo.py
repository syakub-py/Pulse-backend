from datetime import datetime
from typing import Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from App.LoggerConfig import pulse_logger as logger
from App.DB.Session import session_scope as session
from App.DB.Models.Todo import Todo
import ollama
from dotenv import load_dotenv
import os
from ollama import Message
from App.EndpointInputModels.TodoDetails import TodoDetails

load_dotenv()

def addTodo(todo: TodoDetails) -> Dict[str, Any]:
    if not todo:
        return {"message": "No todo details were provided", "status_code": 400}

    try:
        with session() as db_session:
            logger.info(f"Adding Todo to property id: {todo.PropertyId}")

            system_prompt = Message(role="system", content="""You are an expert assistant specializing in recommending professionals to resolve property management issues. When the user provides a description of a problem, your task is to identify the most appropriate type of professional or service provider to address the issue. Your response should always consist of just the professional's title, without any additional information.""")
            user_message = Message(role="user", content=todo.Description)
            messages_list = [system_prompt, user_message]

            model = os.getenv("CHAT_MODEL")
            if not model:
                return {"message": "Chat model not found in environment variables", "status_code": 500}

            try:
                aiResponse = ollama.chat(model, messages=messages_list)
                professional = aiResponse['message']['content']
            except Exception as e:
                logger.error(f"Error getting AI response: {e}")
                professional = "Unknown"

            new_todo = Todo(
                property_id=todo.PropertyId,
                title=todo.Title,
                description=todo.Description,
                status=todo.Status,
                priority=todo.Priority,
                added_by=todo.AddedBy,
                recommended_professional=str(professional).replace(" ", "_"),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            db_session.add(new_todo)
            db_session.commit()
            db_session.refresh(new_todo)

            return {"todo_id": new_todo.todo_id, "status_code": 201}

    except SQLAlchemyError as e:
        logger.error(f"Database error adding the todo: {e}")
        return {"message": "Database error occurred", "status_code": 500}
    except Exception as e:
        logger.error(f"Error adding the todo: {e}")
        return {"message": "An unexpected error occurred", "status_code": 500}
