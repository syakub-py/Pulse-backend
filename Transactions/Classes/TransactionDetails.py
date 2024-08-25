from pydantic import BaseModel


class TransactionDetails(BaseModel):
    userId: str
    propertyId: int
    amount: int
    description: str
    transactionType: str
    incomeOrExpense: str
