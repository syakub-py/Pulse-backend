from sqlalchemy import or_
from DB.ORM.Models.Chat import Chat
from DB.ORM.Models.ChatParticipant import ChatParticipant
from DB.ORM.Utils.Session import session_scope as session
from LoggerConfig import pulse_logger as logger


def createChat(partyOneId: int, partyTwoId: int):
    try:
        if partyOneId == partyTwoId:
            return {"message": "landlord and tenant are the same", "status_code": 500}

        with session() as db_session:
            existing_chat = db_session.query(Chat).filter(
                or_(
                    Chat.last_message_sender_id == partyOneId,
                    Chat.last_message_sender_id == partyTwoId
                )
            ).first()
            if existing_chat:
                logger.info('Chat already exists')
                return existing_chat.chat_id

            new_chat = Chat()
            db_session.add(new_chat)
            db_session.flush()

            participant_one = ChatParticipant(chat_id=new_chat.chat_id, user_id=partyOneId)
            participant_two = ChatParticipant(chat_id=new_chat.chat_id, user_id=partyTwoId)
            db_session.add(participant_one)
            db_session.add(participant_two)

            db_session.commit()
            logger.info('Successfully created chat')
            return new_chat.chat_id
    except Exception as e:
        logger.error(f"Error creating Chat: {str(e)}")
        db_session.rollback()
        return {"message": str(e), "status_code": 500}
