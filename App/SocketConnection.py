import json
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from typing import Dict
from App.Utils.Chats.SaveMessageToDB import saveMessageToDB
from App.LoggerConfig import pulse_logger as logger

router = APIRouter()

active_users: Dict[int, WebSocket] = {}

@router.websocket("/ws/")
async def handle_websocket_connection(websocket: WebSocket, senderUserToken: int, receiverUserToken: int):
    try:
        await websocket.accept()
        active_users[senderUserToken] = websocket
        print(f"{senderUserToken} connected. Active users: {list(active_users.keys())}")
        while True:
            if senderUserToken and receiverUserToken:
                data = await websocket.receive_text()
                json_data = json.loads(data)
                message = json_data['details']
                saveMessageToDB(json_data["chat_id"], message["text"], senderUserToken)
                if is_user_active(receiverUserToken):
                    otherUserWebsocket = active_users[receiverUserToken]
                    try:
                        data = {
                            "_id": message["_id"],
                            "text": message["text"],
                            "createdAt": message["createdAt"],
                            "user": {
                                "_id": message["user"]["_id"],
                                "name": message["user"]["name"],
                                "avatar": getattr(message, "avatar", "")
                            }
                        }

                        await otherUserWebsocket.send_text(json.dumps(data))
                    except Exception as e:
                        logger.error(f"{senderUserToken} disconnected. Active users: {list(active_users.keys())}")
    except WebSocketDisconnect:
        logger.info(f"{senderUserToken} disconnected. Active users: {list(active_users.keys())}")

    finally:
        if senderUserToken in active_users:
            del active_users[senderUserToken]

def is_user_active(uid: int) -> bool:
    return uid in active_users


