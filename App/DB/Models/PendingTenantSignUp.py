from sqlalchemy import Column, Integer, String, Boolean, Date
from App.DB.Base import Base

class PendingTenantSignUp(Base):
    __tablename__ = 'pending_tenant_sign_up'
    pending_tenant_sign_up_id = Column(Integer, primary_key=True, autoincrement=True)
    lease_id = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    is_code_used = Column(Boolean, nullable=False)
    expires = Column(Date, nullable=False)
