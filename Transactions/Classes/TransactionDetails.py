from pydantic import BaseModel


class TransactionDetails(BaseModel):
    userId: str
    amount: int
    description: str
    transactionType: str
