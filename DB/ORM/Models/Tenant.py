from DB.ORM.Base import Base
from sqlalchemy import Column, String, Integer


class Tenant(Base):
    __tablename__ = 'tenants'
    tenant_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
