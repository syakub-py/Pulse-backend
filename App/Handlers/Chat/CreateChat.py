from sqlalchemy import or_
from App.DB.Models.Chat import Chat
from App.DB.Models.ChatParticipant import ChatParticipant
from App.DB.Session import session_scope as session
from App.LoggerConfig import pulse_logger as logger
from typing import Dict, Any, Optional
from sqlalchemy import select

def createChat(partyOneId: int, partyTwoId: int) ->  Optional[Dict[str, Any]]:
    try:
        if partyOneId == partyTwoId:
            return {"message": "landlord and tenant are the same", "status_code": 500}

        with session() as db_session:
            chat_select_stmt = (
                select(Chat)
                .filter(
                    or_(
                        Chat.last_message_sender_id == partyOneId,
                        Chat.last_message_sender_id == partyTwoId
                    )
                )
            )

            chat_result = db_session.execute(chat_select_stmt).scalars().first()

            if chat_result:
                logger.info('Chat already exists')

            new_chat = Chat()
            db_session.add(new_chat)
            db_session.flush()

            participant_one = ChatParticipant(chat_id=new_chat.chat_id, user_id=partyOneId)
            participant_two = ChatParticipant(chat_id=new_chat.chat_id, user_id=partyTwoId)
            db_session.add(participant_one)
            db_session.add(participant_two)

            db_session.commit()
            logger.info('Successfully created chat')
            return {"message": "Chat successfully created", "status_code": 201}
    except Exception as e:
        logger.error(f"Error creating Chat: {str(e)}")
        db_session.rollback()
        return {"message": f"Error creating Chat: {str(e)}", "status_code": 500}
