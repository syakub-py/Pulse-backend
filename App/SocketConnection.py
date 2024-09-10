from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from typing import Dict

router = APIRouter()

# Dictionary to map user IDs to their WebSocket connections
active_users: Dict[int, WebSocket] = {}

def get_active_users() -> Dict[int, WebSocket]:
    return active_users

@router.websocket("/ws/")
async def init_websocket_connection(websocket: WebSocket, token: int):
    try:
        await websocket.accept()
        active_users[token] = websocket
        print(f"{token} connected. Active users: {list(active_users.keys())}")

        while True:
            try:
                data = await websocket.receive_text()
                print(f"Received data from {token}: {data}")
            except WebSocketDisconnect:
                break

    except WebSocketDisconnect:
        pass
    finally:
        if token in active_users:
            del active_users[token]
            print(f"{token} disconnected. Active users: {list(active_users.keys())}")

def isUserActive(uid: int) -> bool:
    return uid in active_users

async def sendMessage(user_id: int, message: str) -> dict:
    if isUserActive(user_id):
        websocket = active_users[user_id]
        try:
            await websocket.send_text(message)
            return {"status": "success", "message": "Message sent successfully"}
        except WebSocketDisconnect:
            return {"status": "error", "message": "WebSocket disconnected"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to send message: {str(e)}"}
    else:
        return {"status": "error", "message": "User not active or not connected"}
