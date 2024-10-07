import json
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from typing import Dict
from asyncio import Lock
from App.Utils.Chats.SaveMessageToDB import saveMessageToDB
from App.LoggerConfig import pulse_logger as logger

router = APIRouter()
active_users: Dict[int, WebSocket] = {}
user_lock = Lock()

@router.websocket("/ws/chat/")
async def handleWebsocketConnection(websocket: WebSocket, senderUserToken: int, receiverUserToken: int):
    try:
        await websocket.accept()
        async with user_lock:
            active_users[senderUserToken] = websocket
        logger.info(f"{senderUserToken} connected. Active users: {list(active_users.keys())}")

        while True:
            if senderUserToken and receiverUserToken:
                try:
                    data = await websocket.receive_text()
                    json_data = json.loads(data)
                    message = json_data.get('details', {})
                    if not message or 'text' not in message:
                        logger.error(f"Invalid message format from {senderUserToken}")
                        return {"message": f"Invalid message format from {senderUserToken}", "status_code": 500}

                    saveMessageToDB(json_data["chat_id"], message["text"], senderUserToken)

                    if isUserActive(receiverUserToken):
                        otherUserWebsocket = active_users[receiverUserToken]
                        await sendMessage(otherUserWebsocket, message)
                except (json.JSONDecodeError, ValueError) as e:
                    logger.error(f"Failed to parse message from {senderUserToken}: {e}")
                except Exception as e:
                    logger.error(f"Failed to send message: {str(e)}")
                    async with user_lock:
                        if receiverUserToken in active_users:
                            del active_users[receiverUserToken]

    except WebSocketDisconnect:
        logger.info(f"{senderUserToken} disconnected. Notifying {receiverUserToken} if active.")
    finally:
        async with user_lock:
            if senderUserToken in active_users:
                del active_users[senderUserToken]

def isUserActive(uid: int) -> bool:
    return uid in active_users

async def sendMessage(websocket: WebSocket, message: dict):
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
    await websocket.send_text(json.dumps(data))
