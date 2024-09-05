from fastapi import APIRouter
from LoggerConfig import pulse_logger as logger
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Todo import Todo
from typing import Union, Dict, Any
from sqlalchemy import select

router = APIRouter()


@router.delete("/todo/deleteTodo/{todo_id}")
def deleteTodo(todo_id: int) -> Union[None, Dict[str, Any]]:
    if not todo_id:
        return {"message": "todo_id was not provided", "status_code": 500}
    try:
        with session() as db_session:
            todo_filter_stmt = select(Todo).filter(Todo.todo_id == todo_id)
            result = db_session.execute(todo_filter_stmt).scalars().first()

            if result is None:
                return {"message": "todo not found", "status_code": 500}

            db_session.delete(result)
            db_session.commit()
            logger.info(f'Deleted todo {todo_id}')
        return None
    except Exception as e:
        logger.error(e)
        return {"message": str(e), "status_code": 500}
