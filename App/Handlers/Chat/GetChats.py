from sqlalchemy import select
from fastapi import APIRouter
from sqlalchemy.orm import aliased
from typing import Union, Dict, Any
from App.DB.Models.Chat import Chat
from App.DB.Models.ChatParticipant import ChatParticipant
from App.DB.Models.User import User
from App.DB.Utils.Session import session_scope as session

router = APIRouter()

@router.get("/chat/getChats/{userId}")
def getChats(userId: int) -> Union[list[Dict[str, Any]], Dict[str, Any]]:
    try:
        with session() as db_session:
            ChatParticipantAlias = aliased(ChatParticipant)
            UserAlias = aliased(User)

            chats_stmt = (
                select(Chat)
                .join(ChatParticipant)
                .filter(ChatParticipant.user_id == userId)
            )

            chats = db_session.execute(chats_stmt).scalars().all()

            if not chats:
                return {"message": "No chats found", "status_code": 404}

            chats_data = []
            for chat in chats:
                other_participant_stmt = (
                    select(ChatParticipantAlias)
                    .filter(
                        ChatParticipantAlias.chat_id == int(chat.chat_id),
                        ChatParticipantAlias.user_id != int(userId)
                    )
                )

                other_participant_result = db_session.execute(other_participant_stmt).scalars().first()

                if other_participant_result is None:
                    continue

                if other_participant_result.user_id == 0:
                    chats_data.append({
                        "chatId": chat.chat_id,
                        "LastMessage": chat.last_message,
                        "OtherUserDetails": {
                            "userId": 0,
                            "Name": "Pulse AI",
                            "PhoneNumber": "",
                            "Email": "",
                            "AnnualIncome": "",
                            "DateOfBirth": "",
                            "DocumentType": "",
                            "DocumentProvidedUrl": "",
                            "SocialSecurity": "",
                        },
                        "Messages": [message.message_content for message in chat.messages]
                    })
                else:
                    other_user_stmt = select(UserAlias).filter(UserAlias.user_id == other_participant_result.user_id)
                    other_user_result = db_session.execute(other_user_stmt).scalars().first()

                    if other_user_result is None:
                        continue

                    chats_data.append({
                        "chatId": chat.chat_id,
                        "LastMessage": chat.last_message,
                        "OtherUserDetails": {
                            "userId": other_user_result.user_id,
                            "Name": other_user_result.name,
                            "PhoneNumber": other_user_result.phone_number,
                            "Email": other_user_result.email,
                            "AnnualIncome": other_user_result.annual_income,
                            "DateOfBirth": other_user_result.date_of_birth,
                            "DocumentType": other_user_result.document_type,
                            "DocumentProvidedUrl": other_user_result.document_provided_url,
                            "SocialSecurity": other_user_result.social_security,
                        },
                        "Messages": [message.message_content for message in chat.messages]
                    })

            return chats_data
    except Exception as e:
        return {"message": str(e), "status_code": 500}
