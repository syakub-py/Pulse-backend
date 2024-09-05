from typing import Dict
from fastapi import APIRouter
from App.Handlers.Users.AddAUser import addAUser
from App.Handlers.Users.DeleteAUser import deleteAUser
from App.Handlers.Users.GetUid import getUid
from App.Models.UserDetails import UserDetails

usersRoutes = APIRouter(prefix="/user")

@usersRoutes.get("/getUid/{firebase_uid}/{username}", response_model=Dict)
async def get_uid(firebase_uid: str, username: str):
    return getUid(firebase_uid, username)

@usersRoutes.get("/addUser/", response_model=Dict)
async def add_a_user(user: UserDetails):
    return addAUser(user)

@usersRoutes.delete("/deleteUser/{userId}", response_model=Dict)
async def delete_a_user(userId: int):
    return deleteAUser(userId)

