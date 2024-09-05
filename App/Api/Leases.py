from typing import Dict, Any
from fastapi import APIRouter
from App.Handlers.Leases.AddLease import addLease
from Models.LeaseDetails import LeaseDetails
from App.Handlers.Leases.DeleteLease import deleteLease
from App.Handlers.Leases.GetLeases import getLeases

leasesRoutes = APIRouter(prefix="/lease")

@leasesRoutes.post("/addLease/{propertyId}", response_model=Dict)
def add_lease(propertyId: int, lease: LeaseDetails) -> (int | Dict[str, Any]):
    return addLease(propertyId, lease)

@leasesRoutes.delete("/deleteLease/{leaseId}", response_model=Dict)
def delete_lease(leaseId: int) -> (Dict[str, Any] | None):
    return deleteLease(leaseId)

@leasesRoutes.get("/getLeases/{property_id}", response_model=Dict)
def get_leases(property_id: int) -> (str | Dict[str, Any]):
    return getLeases(property_id)
