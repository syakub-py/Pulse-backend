from datetime import datetime

from fastapi import APIRouter
from LoggerConfig import pulse_logger as logger
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Todo import Todo

from .Classes.TodoDetails import TodoDetails

router = APIRouter()

@router.post("/todo/addTodo/")
def addTodo(todo: TodoDetails):
    try:
        with session() as db_session:
            logger.info("Adding Todo to property id: {}".format(todo.PropertyId))
            new_todo = Todo(
                property_id=todo.PropertyId,
                title=todo.Title,
                description=todo.Description,
                status=todo.Status,
                priority=todo.Priority,
                added_by=todo.AddedBy,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            db_session.add(new_todo)
            db_session.commit()

            db_session.refresh(new_todo)

            return {"RecommendedProfessional": "Todo created successfully", "todo_id": new_todo.id}
    except Exception as e:
        logger.error("Error adding the todo: {}".format(e))
        db_session.rollback()
        return {"error": str(e)}
    finally:
        db_session.close()






