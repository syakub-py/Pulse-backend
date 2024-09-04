from fastapi import APIRouter
from sqlalchemy.orm import aliased
from DB.ORM.Models.Chat import Chat
from DB.ORM.Models.ChatParticipant import ChatParticipant
from DB.ORM.Models.User import User
from DB.ORM.Utils.Session import session_scope as session

router = APIRouter()

@router.get("/chat/getChats/{userId}")
def getChats(userId: int):
    try:
        with session() as db_session:
            ChatParticipantAlias = aliased(ChatParticipant)
            UserAlias = aliased(User)

            chats_query = db_session.query(Chat).join(ChatParticipant).filter(ChatParticipant.user_id == userId)

            chats = chats_query.all()

            if not chats:
                return {"message": "No chats found", "status_code": 404}

            chats_data = []
            for chat in chats:
                other_participant = (
                    db_session.query(ChatParticipantAlias)
                    .filter(
                        ChatParticipantAlias.chat_id == int(chat.chat_id),
                        ChatParticipantAlias.user_id != int(userId)
                    )
                    .first()
                )
                if other_participant:
                    if other_participant.user_id == 0:
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
                        other_user = db_session.query(UserAlias).filter(UserAlias.user_id == other_participant.user_id).first()
                        if other_user:
                            chats_data.append({
                                "chatId": chat.chat_id,
                                "LastMessage": chat.last_message,
                                "OtherUserDetails": {
                                    "userId": other_user.user_id,
                                    "Name": other_user.name,
                                    "PhoneNumber": other_user.phone_number,
                                    "Email": other_user.email,
                                    "AnnualIncome": other_user.annual_income,
                                    "DateOfBirth": other_user.date_of_birth,
                                    "DocumentType": other_user.document_type,
                                    "DocumentProvidedUrl": other_user.document_provided_url,
                                    "SocialSecurity": other_user.social_security,
                                },
                                "Messages": [message.message_content for message in chat.messages]
                            })

            return chats_data
    except Exception as e:
        return {"message": str(e), "status_code": 500}
