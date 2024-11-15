from App.DB.Base import Base

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class PropertyLease(Base):
    __tablename__ = 'property_lease'
    property_lease_id = Column(Integer, primary_key=True, autoincrement=True)

    property_id = Column(Integer, ForeignKey('property.property_id'))
    lease_id = Column(Integer, ForeignKey('lease.lease_id'), unique=True)

    property = relationship("Property", back_populates="leases")
    lease = relationship("Lease", back_populates="properties")
