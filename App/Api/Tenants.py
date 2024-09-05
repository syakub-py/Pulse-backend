from typing import Dict
from fastapi import APIRouter
from App.Handlers.Tenants.CheckTenantCode import checkTenantCode
from App.Handlers.Tenants.GetTenants import getTenants

tenantRoutes = APIRouter(prefix="/tenant")

@tenantRoutes.get("/checkTenantCode/{tenantCode}", response_model=Dict)
async def check_tenant_code(tenantCode: str):
    return checkTenantCode(tenantCode)

@tenantRoutes.get("/getTenants/{userId}", response_model=Dict)
async def get_tenants(userId: int):
    return getTenants(userId)
