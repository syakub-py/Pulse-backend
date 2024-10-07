from typing import Dict, Any
from fastapi import APIRouter
from App.Handlers.Emails.SendEmail import sendEmail

emailRoutes = APIRouter(prefix="/api")

@emailRoutes.get("/sendEmail/{leaseId}/{tenantEmail}", response_model=Dict)
def send_email(tenantEmail: str, leaseId: int) -> Dict[str, Any]:
    return sendEmail(tenantEmail, leaseId)
