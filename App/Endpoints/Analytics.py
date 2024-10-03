from fastapi import APIRouter
from typing import Dict, Any
from App.Handlers.Analytics.GenerateExpenseAnalytics import generateExpenseAnalytics
from App.Handlers.Analytics.GenerateIncomeAnalytics import generateIncomeAnalytics

analyticsRoutes = APIRouter(prefix="/analytics")

@analyticsRoutes.get("/generateExpenseAnalytics/{propertyId}", response_model=Dict)
def generate_expense_analytics(property_id: int) -> (Dict[str, Any] | list[dict[str, Any]]):
    return generateExpenseAnalytics(property_id)

@analyticsRoutes.get("/generateIncomeAnalytics/{propertyId}")
def generate_income_analytics(propertyId: int) -> Dict[str, Any]:
    return generateIncomeAnalytics(propertyId)
