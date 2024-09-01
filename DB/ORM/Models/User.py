from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship

from DB.ORM.Base import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    firebase_uid = Column(String(255), unique=True, nullable=False)
    name = Column(String, nullable=False)
    annual_income = Column(Integer, nullable=False)
    phone_number = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False)
    email = Column(String, nullable=False)
    document_provided_url = Column(String, nullable=False)
    document_type = Column(String, nullable=False)
    social_security = Column(String, nullable=False)
    created_at = Column(Date, server_default=datetime.now().strftime('%Y-%m-%d'))
    leases = relationship("TenantLease", back_populates="tenant")
