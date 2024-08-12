from datetime import datetime

from fastapi import APIRouter
from LoggerConfig import pulse_logger as logger
from DB.ORM.Utils.Session import session_scope as session
from DB.ORM.Models.Todo import Todo

router = APIRouter()



@router.post("/Todo/AddTodo/")
def AddTodo(todo:Todo):
    try:
        with session() as db_session:
            logger.info("Adding Todo to property id: {}".format(todo.property_id))
            new_todo = Todo(
                property_id=todo.property_id,
                title=todo.title,
                description=todo.description,
                status=todo.status,
                priority=todo.priority,
                added_by=todo.added_by,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            db_session.add(new_todo)
            db_session.commit()

            db_session.refresh(new_todo)

            return {"message": "Todo created successfully", "todo_id": new_todo.id}
    except Exception as e:
        logger.info("error adding the todo: {}".format(e))
        db_session.rollback()
    finally:
        db_session.close()





