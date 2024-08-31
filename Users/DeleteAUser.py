from fastapi import APIRouter
from DB.ORM.Models.User import User
from DB.ORM.Utils.Session import session_scope as session

router = APIRouter()


@router.delete('/user/deleteUser/{uid}')
def deleteAUser(uid: str):
    try:
        with session() as db_session:
            user = db_session.query(User).filter(User.firebase_uid == uid).first()
            if user is None:
                return {"message": "User not found", "status_code": 500}

            db_session.delete(user)
            db_session.commit()
    except Exception as e:
        return {"message": str(e), "status_code": 500}

