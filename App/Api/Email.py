from typing import Dict, Any
from fastapi import APIRouter
from App.Handlers.Emails.SendEmail import sendEmail

emailRoutes = APIRouter(prefix="/api")

@emailRoutes.get("/sendEmail/{LeaseId}/{tenantEmail}", response_model=Dict)
def send_email(tenantEmail: str, LeaseId: int) -> (None | Dict[str, Any]):
    return sendEmail(tenantEmail, LeaseId)
