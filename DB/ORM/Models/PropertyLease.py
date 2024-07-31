from DB.ORM.Base import Base

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class PropertyLease(Base):
    __tablename__ = 'property_leases'

    property_id = Column(Integer, ForeignKey('properties.property_id'), primary_key=True)
    lease_id = Column(Integer, ForeignKey('leases.lease_id'), primary_key=True)

    property = relationship("Property", back_populates="leases")
    lease = relationship("Lease", back_populates="properties")
