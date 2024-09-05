from typing import Dict
from fastapi import APIRouter
from App.Handlers.Leases.AddLease import addLease
from Models.LeaseDetails import LeaseDetails
from App.Handlers.Leases.DeleteLease import deleteLease
from App.Handlers.Leases.GetLeases import getLeases

leasesRoutes = APIRouter(prefix="/lease")

@leasesRoutes.post("/addLease/{propertyId}", response_model=Dict)
async def add_lease(propertyId: int, lease: LeaseDetails):
    return addLease(propertyId, lease)

@leasesRoutes.delete("/deleteLease/{leaseId}", response_model=Dict)
async def delete_lease(leaseId: int):
    return deleteLease(leaseId)

@leasesRoutes.get("/getLeases/{property_id}", response_model=Dict)
async def get_leases(property_id: int):
    return getLeases(property_id)
