import json
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from typing import Dict

from App.EndpointInputModels.MessageDetails import MessageDetails
from App.Utils.Chats.SaveMessageToDB import saveMessageToDB

router = APIRouter()

active_users: Dict[int, WebSocket] = {}

@router.websocket("/ws/")
async def handle_websocket_connection(websocket: WebSocket, token: int, otherUserToken: int):
    try:
        await websocket.accept()
        active_users[token] = websocket
        print(f"{token} connected. Active users: {list(active_users.keys())}")

        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            if token:
                print(f"{token} received {json_data}")
                await send_message(otherUserToken, json_data["details"])
                # Uncomment if you want to save messages to the database
                # saveMessageToDB(json_data["chat_id"], json_data["details"]["text"], token)

    except WebSocketDisconnect:
        print(f"{token} disconnected. Active users: {list(active_users.keys())}")
    finally:
        if token in active_users:
            del active_users[token]

def is_user_active(uid: int) -> bool:
    return uid in active_users

async def send_message(user_id: int, message: MessageDetails) -> dict:
    print("Is other user active: " + str(is_user_active(user_id)))

    if is_user_active(user_id):
        websocket = active_users[user_id]
        try:
            data = {
                '_id': message.id,
                'text': message.text,
                'createdAt': message.createdAt,
                'user': {
                    '_id': message.user.id,
                    'name': message.user.name,
                    'avatar': getattr(message, 'userAvatar', None)
                }
            }
            await websocket.send_text(json.dumps(data))  # Use json.dumps to serialize properly
            return {"status": "success", "message": "Message sent successfully"}
        except WebSocketDisconnect:
            return {"status": "error", "message": "WebSocket disconnected"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to send message: {str(e)}"}
    else:
        return {"status": "error", "message": "User not active or not connected"}
