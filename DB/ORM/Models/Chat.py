from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship
from DB.ORM.Base import Base


class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    messages = relationship("Message", back_populates="chat")
