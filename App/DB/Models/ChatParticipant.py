from sqlalchemy import Column, Integer, ForeignKey
from DB.ORM.Base import Base

class ChatParticipant(Base):
    __tablename__ = 'chat_participant'
    chat_participant_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, ForeignKey('chat.chat_id'), nullable=False)
