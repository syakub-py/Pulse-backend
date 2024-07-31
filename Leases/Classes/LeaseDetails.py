from pydantic import BaseModel

class LeaseDetails(BaseModel):
    StartDate: str
    EndDate: str
    MonthlyRent: str
    PropertyId: int
