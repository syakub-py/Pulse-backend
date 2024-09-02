from fastapi import WebSocket, WebSocketDisconnect, APIRouter

router = APIRouter()

active_users = set()


def get_active_users():
    return active_users


@router.websocket("/ws/")
async def init_websocket_connection(websocket: WebSocket, token: str):
    try:
        await websocket.accept()
        active_users.add(token)
        print(f"{token} connected. Active users: {list(active_users)}")

    except WebSocketDisconnect:
        active_users.remove(token)
        print(f"{token} disconnected. Active users: {list(active_users)}")


def isUserActive(uid: int):
    return uid in active_users
