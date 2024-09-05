from fastapi import APIRouter
from LoggerConfig import pulse_logger as logger
from App.DB.Utils.Session import session_scope as session
from App.DB.Models.Todo import Todo
from typing import Union, Dict, Any
from sqlalchemy import delete

router = APIRouter()


@router.delete("/todo/deleteTodo/{todo_id}")
def deleteTodo(todo_id: int) -> Union[None, Dict[str, Any]]:
    if not todo_id:
        return {"message": "todo_id was not provided", "status_code": 500}
    try:
        with session() as db_session:
            todo_delete_stmt = delete(Todo).where(Todo.todo_id == todo_id)
            result = db_session.execute(todo_delete_stmt)

            if result.rowcount == 0:
                return {"message": "todo not found", "status_code": 500}

            db_session.commit()
            logger.info(f'Deleted todo {todo_id}')
        return None
    except Exception as e:
        logger.error(e)
        return {"message": str(e), "status_code": 500}
