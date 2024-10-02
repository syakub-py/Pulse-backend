import json

from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from typing import Dict

from App.Models.MessageDetails import Message
from App.Utils.Chats.SaveMessageToDB import saveMessageToDB

router = APIRouter()

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
                json_data = json.loads(data)
                if token:
                    print(json_data["chat"]["chat_id"], json_data["chat"]["details"]["text"])
                    # await sendMessage(token, json_data)
                    # saveMessageToDB(json_data["Message"]["chat_id"], json_data["Message"]["details"]["text"], token)

                print(f"Received data from {token}: {json_data}")
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


async def sendMessage(user_id: int, message: Message) -> dict:
    if isUserActive(user_id):
        websocket = active_users[user_id]
        try:
            data = {
                '_id': message.id,
                'text': message.text,
                'createdAt': message.createdAt,
                'user': {
                    '_id': message.user.id,
                    'name': message.email if hasattr(message, 'email') else "Pulse AI",
                    'avatar': getattr(message, 'userAvatar', None)
                }
            }

            await websocket.send_text(str(data))
            return {"status": "success", "message": "Message sent successfully"}
        except WebSocketDisconnect:
            return {"status": "error", "message": "WebSocket disconnected"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to send message: {str(e)}"}
    else:
        return {"status": "error", "message": "User not active or not connected"}
