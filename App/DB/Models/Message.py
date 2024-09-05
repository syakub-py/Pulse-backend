from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from DB.ORM.Base import Base

class Message(Base):
    __tablename__ = 'message'
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chat.chat_id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(String(60), nullable=True)

    chat = relationship("Chat", back_populates="messages")
