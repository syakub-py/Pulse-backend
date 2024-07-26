from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from DB.ORM.Base import Base

class Property(Base):
    __tablename__ = 'properties'
    property_id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=False)
    nick_name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    property_type = Column(String(255), nullable=False)
    is_rental = Column(Boolean, nullable=False, default=False)
    created_at = Column(String, default=datetime.now().strftime("%a %b %d %Y %H:%M:%S"))
    # smart_devices = relationship("SmartDevice", back_populates="property")
    # transactions = relationship("Transaction", back_populates="property")
    # todos = relationship("Todo", back_populates="property")
