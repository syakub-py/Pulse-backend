from typing import Dict, Any
from fastapi import APIRouter
from App.Handlers.Transactions.GetTransactions import getTransactions
from App.Handlers.Transactions.AddTransaction import addTransaction
from App.EndpointParams.TransactionDetails import TransactionDetails

transactionsRoutes = APIRouter(prefix="/transaction")

@transactionsRoutes.get("/getTransaction/{propertyId}", response_model=Dict)
def get_transactions(propertyId: int) -> Dict[str, Any]:
    return getTransactions(propertyId)

@transactionsRoutes.post("/addTransaction/", response_model=Dict)
def add_transaction(transaction: TransactionDetails) ->Dict[str, Any]:
    return addTransaction(transaction)
