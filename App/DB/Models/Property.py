from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from DB.ORM.Base import Base

class Property(Base):
    __tablename__ = 'property'
    property_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    firebase_uid = Column(String(255), nullable=False)
    nick_name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    property_type = Column(String(255), nullable=False)
    is_rental = Column(Boolean, nullable=False, default=False)
    purchase_price = Column(String(255))
    operating_expenses = Column(String(255))
    property_tax = Column(String(255))
    mortgage_payment = Column(String(255))
    created_at = Column(String, default=lambda: datetime.now().strftime("%a %b %d %Y %H:%M:%S"))
    leases = relationship("PropertyLease", back_populates="property")
    todos = relationship("Todo", back_populates="property")
    transactions = relationship("Transaction", back_populates="property")
