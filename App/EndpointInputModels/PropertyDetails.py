from pydantic import BaseModel

class PropertyDetails(BaseModel):
    Name: str
    Address: str
    PropertyType: str
    isRental: bool
    PurchasePrice: str
    Taxes: str
    MortgagePayment: str
    OperatingExpenses: str
