from typing import Optional

from pydantic import BaseModel

class UserDetails(BaseModel):
    Name: str
    UserId: str
    LeaseId: Optional[int] = None
    AnnualIncome: int
    PhoneNumber: str
    DateOfBirth: str
    Email: str
    DocumentProvidedUrl: str
    DocumentType: str
    SocialSecurity: str
