from sqlalchemy import Column, Integer, String, Boolean, Date
from DB.ORM.Base import Base

class PendingTenantSignUp(Base):
    __tablename__ = 'pending_tenant_sign_ups'
    id = Column(Integer, primary_key=True, index=True)
    lease_id = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    is_code_used = Column(Boolean, nullable=False)
    expires = Column(Date, nullable=False)
