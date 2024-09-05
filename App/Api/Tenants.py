from typing import Dict, Any
from fastapi import APIRouter
from App.Handlers.Tenants.CheckTenantCode import checkTenantCode
from App.Handlers.Tenants.GetTenants import getTenants

tenantRoutes = APIRouter(prefix="/tenant")

@tenantRoutes.get("/checkTenantCode/{tenantCode}", response_model=Dict)
def check_tenant_code(tenantCode: str) -> Dict[str, Any]:
    return checkTenantCode(tenantCode)

@tenantRoutes.get("/getTenants/{userId}", response_model=Dict)
def get_tenants(userId: int) -> (str | Dict[str, Any]):
    return getTenants(userId)
