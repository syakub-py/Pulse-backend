from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from DB.ORM.Base import Base

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), ForeignKey('properties.user_id'))
    property_id = Column(Integer, ForeignKey('properties.property_id'))
    transaction_type = Column(String(50))
    amount = Column(DECIMAL(10, 2))
    description = Column(String(200))
    created_at = Column(String, default=lambda: datetime.now().strftime("%a %b %d %Y %H:%M:%S"))
    property = relationship("Property", back_populates="transactions")
