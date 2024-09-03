from sqlalchemy import Column, Integer, ForeignKey, DateTime

from DB.ORM.Base import Base


class ChatParticipant(Base):
    __tablename__ = 'chat_participant'
    chat_participant_id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chat.chat_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    # join_date = Column(DateTime, nullable=False)
