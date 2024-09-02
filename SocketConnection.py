from fastapi import WebSocket, WebSocketDisconnect, Depends, APIRouter
from typing import List

router = APIRouter()

active_users = set()

def get_active_users():
    return active_users

@router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, token: str):
    await websocket.accept()
    active_users.add(token)
    print(f"{token} connected. Active users: {list(active_users)}")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data from {token}: {data}")
            # Here you can handle incoming messages

    except WebSocketDisconnect:
        active_users.remove(token)
        print(f"{token} disconnected. Active users: {list(active_users)}")

@router.get("/active_users/", response_model=List[str])
async def get_active_users_endpoint(active_users: set = Depends(get_active_users)):
    return list(active_users)

