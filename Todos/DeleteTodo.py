from fastapi import APIRouter
from LoggerConfig import pulse_logger as logger
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Todo import Todo
from typing import Union, Dict, Any

router = APIRouter()


@router.delete("/todo/deleteTodo/{todo_id}")
def deleteTodo(todo_id: int) -> Union[None, Dict[str, Any]]:
    if not todo_id:
        return {"message": "todo_id was not provided", "status_code": 500}
    try:
        with session() as db_session:
            todo = db_session.query(Todo).filter(Todo.id == todo_id).first()
            db_session.delete(todo)
            db_session.commit()
            logger.info(f'Deleted todo {todo_id}')
        return None
    except Exception as e:
        logger.error(e)
        return {"message": str(e), "status_code": 500}
