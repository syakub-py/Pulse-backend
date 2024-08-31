from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from DB.ORM.Base import Base


class TenantLease(Base):
    __tablename__ = 'tenant_lease'
    tenant_lease_id = Column(Integer, primary_key=True, autoincrement=True)

    tenant_id = Column(Integer, ForeignKey('user.id'))
    lease_id = Column(Integer, ForeignKey('lease.lease_id'))

    tenant = relationship("User", back_populates="leases")
    leases = relationship("Lease", back_populates="tenants")
