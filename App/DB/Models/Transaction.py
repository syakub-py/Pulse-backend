from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from App.DB.Base import Base
from decimal import Decimal
from typing import cast

class Transaction(Base):
    __tablename__ = 'transaction'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    property_id = Column(Integer, ForeignKey('property.property_id'))
    transaction_type = Column(String(50))
    income_or_expense = Column(String(50))
    amount = cast(Decimal, Column(DECIMAL(10, 2)))
    description = Column(String(200))
    date = Column(String(40))
    created_at = Column(String, default=lambda: datetime.now().strftime("%a %b %d %Y %H:%M:%S"))
    property = relationship("Property", back_populates="transactions")
