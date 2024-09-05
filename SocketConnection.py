from fastapi import WebSocket, WebSocketDisconnect, APIRouter

router = APIRouter()

active_users: set[str] = set()

def get_active_users() -> set[str]:
    return active_users

@router.websocket("/ws/")
async def init_websocket_connection(websocket: WebSocket, token: str) -> None:
    try:
        await websocket.accept()
        active_users.add(token)
        print(f"{token} connected. Active users: {list(active_users)}")

        return None
    except WebSocketDisconnect:
        active_users.remove(token)
        print(f"{token} disconnected. Active users: {list(active_users)}")
        return None

def isUserActive(uid: int) -> bool:
    return False
    # TODO: Fix this
    # return uid in active_users
