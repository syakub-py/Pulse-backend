from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from DB.ORM.Base import Base


class Todo(Base):
    __tablename__ = 'todo'
    todo_id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey('property.property_id'))
    title = Column(String(100))
    description = Column(String)
    status = Column(String(100))
    priority = Column(String(255))
    added_by = Column(String(100))
    recommended_professional = Column(String(255))
    created_at = Column(Date, default=datetime.now)
    updated_at = Column(Date, default=datetime.now, onupdate=datetime.now)
    property = relationship("Property", back_populates="todos")

