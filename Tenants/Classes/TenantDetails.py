from pydantic import BaseModel


class TenantDetails(BaseModel):
    Name: str
    UserId: str
    LeaseId: int
    AnnualIncome: int
    PhoneNumber: str
    DateOfBirth: str
    Email: str
    DocumentProvidedUrl: str
    SocialSecurity: str

