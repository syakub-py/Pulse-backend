from sqlalchemy import Integer, TIMESTAMP, Text, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from App.DB.Base import Base
from App.DB.Models.Message import Message

class Chat(Base):
    __tablename__ = 'chat'

    chat_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    last_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_message_sender_id: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    messages: Mapped[list[Message]] = relationship("Message", back_populates="chat")
