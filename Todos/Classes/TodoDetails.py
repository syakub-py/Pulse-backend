from pydantic import BaseModel


class TodoDetails(BaseModel):
    PropertyId: int
    Title: str
    Status: str
    Priority: str
    Description: str
    AddedBy: str
