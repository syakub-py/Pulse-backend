from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, CheckConstraint, Text
from sqlalchemy.orm import relationship
from DB.ORM.Base import Base

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))
    role = Column(String(10), CheckConstraint("role IN ('user', 'assistant')"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')

    chat = relationship("Chat", back_populates="messages")
