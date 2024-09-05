from typing import Dict
from fastapi import APIRouter
from App.Handlers.Emails.SendEmail import sendEmail

emailRoutes = APIRouter(prefix="/api")

@emailRoutes.get("/sendEmail/{LeaseId}/{tenantEmail}", response_model=Dict)
async def send_email(tenantEmail: str, LeaseId: int):
    return sendEmail(tenantEmail, LeaseId)
