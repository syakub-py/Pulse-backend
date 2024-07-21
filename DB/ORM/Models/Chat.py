from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from DB.ORM.Base import Base


class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(Integer, primary_key=True)
    user_id = Column(String(255), ForeignKey('properties.user_id'))
    created_at = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')

    messages = relationship("Message", back_populates="chat")
