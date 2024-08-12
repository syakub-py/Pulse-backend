from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from DB.ORM.Base import Base


class TenantLease(Base):
    __tablename__ = 'tenant_leases'

    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'), primary_key=True)
    lease_id = Column(Integer, ForeignKey('leases.lease_id'), primary_key=True)

    tenant = relationship("Tenant", back_populates="leases")
    leases = relationship("Lease", back_populates="tenants")
