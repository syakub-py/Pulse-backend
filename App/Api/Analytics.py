from fastapi import APIRouter
from typing import Dict
from App.Handlers.Analytics.GenerateExpenseAnalytics import generateExpenseAnalytics
from App.Handlers.Analytics.GenerateIncomeAnalytics import generateIncomeAnalytics

analyticsRoutes = APIRouter(prefix="/analytics")

@analyticsRoutes.get("/generateExpenseAnalytics/{propertyId}", response_model=Dict)
async def generate_expense_analytics(property_id: int):
    return generateExpenseAnalytics(property_id)

@analyticsRoutes.get("/generateIncomeAnalytics/{propertyId}")
async def generate_income_analytics(propertyId: int):
    return generateIncomeAnalytics(propertyId)
