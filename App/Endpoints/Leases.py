from typing import Dict, Any
from fastapi import APIRouter
from App.Handlers.Leases.AddLease import addLease
from App.EndpointParams.LeaseDetails import LeaseDetails
from App.Handlers.Leases.DeleteLease import deleteLease
from App.Handlers.Leases.GetLeases import getLeases

leasesRoutes = APIRouter(prefix="/lease")

@leasesRoutes.post("/addLease/{propertyId}", response_model=Dict)
def add_lease(propertyId: int, lease: LeaseDetails) -> Dict[str, Any]:
    return addLease(propertyId, lease)

@leasesRoutes.delete("/deleteLease/{leaseId}", response_model=Dict)
def delete_lease(leaseId: int) -> Dict[str, Any]:
    return deleteLease(leaseId)

@leasesRoutes.get("/getLeases/{propertyId}", response_model=Dict)
def get_leases(propertyId: int) -> Dict[str, Any]:
    return getLeases(propertyId)
