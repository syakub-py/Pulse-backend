from DB.ORM.Base import Base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

class Lease(Base):
    __tablename__ = 'leases'

    lease_id = Column(Integer, primary_key=True)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    monthly_rent = Column(String, nullable=False)
    terms = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
    properties = relationship("PropertyLease", back_populates="lease")
    tenants = relationship("TenantLease", back_populates="leases")
