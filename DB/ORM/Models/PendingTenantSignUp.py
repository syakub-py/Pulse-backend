from sqlalchemy import Column, Integer, String, Boolean
from DB.ORM.Base import Base

class PendingTenantSignUp(Base):
    __tablename__ = 'pending_tenant_sign_ups'
    id = Column(Integer, primary_key=True, index=True)
    lease_id = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    isCodeUsed = Column(Boolean, nullable=False)
