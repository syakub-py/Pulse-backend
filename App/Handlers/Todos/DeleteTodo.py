from App.LoggerConfig import pulse_logger as logger
from App.DB.Session import session_scope as session
from App.DB.Models.Todo import Todo
from typing import Dict, Any
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError

def deleteTodo(todo_id: int) -> Dict[str, Any]:
    if not todo_id:
        return {"message": "todo_id is required", "status_code": 400}

    try:
        with session() as db_session:
            todo_delete_stmt = delete(Todo).where(Todo.todo_id == todo_id)
            result = db_session.execute(todo_delete_stmt)

            if result.rowcount == 0:
                return {"message": "Todo not found", "status_code": 404}

            db_session.commit()
            logger.info(f'Deleted todo {todo_id}')
            return {"message": f"Todo {todo_id} deleted successfully", "status_code": 200}

    except SQLAlchemyError as e:
        logger.error(f"Database error deleting todo {todo_id}: {e}")
        db_session.rollback()
        return {"message": "Database error occurred", "status_code": 500}
    except Exception as e:
        logger.error(f"Unexpected error deleting todo {todo_id}: {e}")
        db_session.rollback()
        return {"message": "An unexpected error occurred", "status_code": 500}
