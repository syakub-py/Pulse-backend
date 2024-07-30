from DB.ORM.Base import Base
from sqlalchemy import Column, Date, String, Float
from sqlalchemy.orm import relationship

class Lease(Base):
    __tablename__ = 'leases'

    lease_id = Column(String, primary_key=True, unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    monthly_rent = Column(Float, nullable=False)

    properties = relationship("PropertyLease", back_populates="lease")
