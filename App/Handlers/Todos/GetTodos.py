from App.DB.Session import session_scope as session
from App.DB.Models.Todo import Todo
from App.LoggerConfig import pulse_logger as logger
from typing import Dict, Any, List
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

def getTodos(propertyId: int) -> Dict[str, Any]:
    if not propertyId:
        return {"message": "propertyId is required", "status_code": 400}

    try:
        with session() as db_session:
            todo_select_stmt = select(Todo).filter(Todo.property_id == propertyId)
            todos = db_session.execute(todo_select_stmt).scalars().all()

            todos_list: List[Dict[str, Any]] = [
                {
                    "id": todo.todo_id,
                    "PropertyId": todo.property_id,
                    "Title": todo.title,
                    "Status": todo.status,
                    "Priority": todo.priority,
                    "Description": todo.description,
                    "AddedBy": todo.added_by,
                    "RecommendedProfessional": todo.recommended_professional,
                    "CreatedAt": todo.created_at.isoformat() if todo.created_at else None,
                    "UpdatedAt": todo.updated_at.isoformat() if todo.updated_at else None,
                }
                for todo in todos
            ]

            if not todos_list:
                return {"message": "No todos found for the given property ID", "status_code": 404}

            return {"data": todos_list, "status_code": 200}

    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving todos for property ID {propertyId}: {e}")
        return {"message": "Database error occurred", "status_code": 500}
    except Exception as e:
        logger.error(f"Unexpected error retrieving todos for property ID {propertyId}: {e}")
        return {"message": "An unexpected error occurred", "status_code": 500}
