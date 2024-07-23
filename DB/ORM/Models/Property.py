from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from DB.ORM.Base import Base

class Property(Base):
    __tablename__ = 'properties'
    property_id = Column(Integer, primary_key=True)
    user_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    country = Column(String(100))
    created_at = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')

    smart_devices = relationship("SmartDevice", back_populates="property")
    transactions = relationship("Transaction", back_populates="property")
    todos = relationship("Todo", back_populates="property")
