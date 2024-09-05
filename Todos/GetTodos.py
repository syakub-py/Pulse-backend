import pandas as pd
from fastapi import APIRouter
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Todo import Todo
from LoggerConfig import pulse_logger as logger
from typing import Union, Dict, Any
from sqlalchemy import select

router = APIRouter()

@router.get("/todo/getTodos/{propertyId}")
def getTodos(propertyId:int) -> Union[str, Dict[str, Any]]:
    if not propertyId:
        return {"message": "propertyId is required", "status_code": 500}
    try:
        with session() as db_session:
            todo_select_stmt = select(Todo).filter(Todo.property_id == propertyId)
            todos = db_session.execute(todo_select_stmt).scalars()

            todos_list = [
                {
                    "id": todo.todo_id,
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
        return {"message": f"Error retrieving todos for property ID {propertyId}: {e}", "status_code":500}
