from pydantic import BaseModel

class LeaseDetails(BaseModel):
    StartDate: str
    EndDate: str
    MonthlyRent: str
    Terms: str
    isLeaseExpired: bool
