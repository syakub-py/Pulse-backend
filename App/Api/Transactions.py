from typing import Dict
from fastapi import APIRouter
from App.Handlers.Transactions.GetTransactions import getTransactions
from App.Handlers.Transactions.AddTransaction import addTransaction
from App.Models.TransactionDetails import TransactionDetails

transactionsRoutes = APIRouter(prefix="/transaction")

@transactionsRoutes.get("/getTransaction/{propertyId}", response_model=Dict)
async def get_transactions(propertyId: int):
    return getTransactions(propertyId)

@transactionsRoutes.get("/addTransaction/", response_model=Dict)
async def add_transaction(transaction: TransactionDetails):
    return addTransaction(transaction)
