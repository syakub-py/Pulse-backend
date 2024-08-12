from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from DB.ORM.Base import Base

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'), nullable=False)
    role = Column(String(10), CheckConstraint("role IN ('user', 'assistant')"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(String(60), nullable=True)

    chat = relationship("Chat", back_populates="messages")
