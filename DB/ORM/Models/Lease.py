from DB.ORM.Base import Base
from sqlalchemy import Column, Date, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime

class Lease(Base):
    __tablename__ = 'leases'

    lease_id = Column(String, primary_key=True, unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    monthly_rent = Column(Float, nullable=False)

    Tenants = relationship('Tenant', back_populates='lease')

    def IsActive(self) -> bool:
        today = datetime.now().date()
        return self.start_date <= today <= self.end_date
