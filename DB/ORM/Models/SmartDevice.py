from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from DB.ORM.Base import Base


class SmartDevice(Base):
    __tablename__ = 'smart_devices'
    device_id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey('properties.property_id'))
    device_name = Column(String(255), nullable=False)
    device_type = Column(String(100))
    device_status = Column(String(50))
    created_at = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')

    property = relationship("Property", back_populates="smart_devices")
