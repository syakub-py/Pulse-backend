from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from DB.ORM.Base import Base

class Property(Base):
    __tablename__ = 'properties'
    property_id = Column(Integer, primary_key=True)
    user_id = Column(String(255), unique=True, nullable=False)
    nick_name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    property_type = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now().strftime("%a %b %d %Y %H:%M:%S GMT%z"))
    # smart_devices = relationship("SmartDevice", back_populates="property")
    # transactions = relationship("Transaction", back_populates="property")
    # todos = relationship("Todo", back_populates="property")
