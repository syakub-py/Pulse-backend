from sqlalchemy.orm import relationship
from DB.ORM.Base import Base
from sqlalchemy import Column, String, Integer


class Tenant(Base):
    __tablename__ = 'tenants'
    tenant_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    annual_income = Column(Integer, nullable=False)
    phone_number = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False)
    email = Column(String, nullable=False)
    document_provided_url = Column(String, nullable=False)
    social_security = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    leases = relationship("TenantLease", back_populates="tenant")
