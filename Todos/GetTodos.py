import pandas as pd
from fastapi import APIRouter
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Todo import Todo
from LoggerConfig import pulse_logger as logger

router = APIRouter()

@router.get("/todo/getTodos/{propertyId}")
def getTodos(propertyId:int):
    try:
        with session() as db_session:
            todos = db_session.query(Todo).filter(Todo.property_id == propertyId).all()

            if not todos:
                return []

            todos_list = [
                {
                    "id": todo.id,
                    "PropertyId": todo.property_id,
                    "Title": todo.title,
                    "Status": todo.status,
                    "Priority": todo.priority,
                    "Description": todo.description,
                    "AddedBy": todo.added_by,
                }
                for todo in todos
            ]

            return pd.DataFrame(todos_list).to_json(orient="records")
    except Exception as e:
        logger.error(f"Error retrieving todos for property ID {propertyId}: {e}")
        return []
