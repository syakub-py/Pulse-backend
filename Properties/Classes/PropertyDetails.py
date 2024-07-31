from pydantic import BaseModel


class PropertyDetails(BaseModel):
    Name: str
    Address: str
    PropertyType: str
    isRental: bool
