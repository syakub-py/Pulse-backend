from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship
from DB.ORM.Base import Base
from App.DB.Models.Message import Message

class Chat(Base):
    __tablename__ = 'chat'
    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    last_message = Column(String(255), nullable=True)
    last_message_sender_id = Column(Integer)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    messages = relationship("Message", back_populates="chat")
