from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from DB.ORM.Base import Base


class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(Integer, primary_key=True)
    user_id = Column(String(255))
    created_at = Column(TIMESTAMP, default= datetime.now().strftime("%a %b %d %Y %H:%M:%S GMT%z"))

    messages = relationship("Message", back_populates="chat")
