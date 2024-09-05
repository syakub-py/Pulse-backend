from typing import Dict, Any
from fastapi import APIRouter
from App.Handlers.Users.AddAUser import addAUser
from App.Handlers.Users.DeleteAUser import deleteAUser
from App.Handlers.Users.GetUid import getUid
from App.Models.UserDetails import UserDetails

usersRoutes = APIRouter(prefix="/user")

@usersRoutes.get("/getUid/{firebase_uid}/{username}", response_model=Dict)
def get_uid(firebase_uid: str, username: str) -> (int | Dict[str, Any]):
    return getUid(firebase_uid, username)

@usersRoutes.get("/addUser/", response_model=Dict)
def add_a_user(user: UserDetails) -> (int | Dict[str, Any]):
    return addAUser(user)

@usersRoutes.delete("/deleteUser/{userId}", response_model=Dict)
def delete_a_user(userId: int) -> (None | Dict[str, Any]):
    return deleteAUser(userId)

