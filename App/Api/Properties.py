from typing import Dict, Any
from fastapi import APIRouter
from App.Models.PropertyDetails import PropertyDetails
from App.Handlers.Properties.AddProperty import addProperty
from App.Handlers.Properties.DeleteProperty import deleteProperty
from App.Handlers.Properties.GetProperties import getProperties

propertiesRoutes = APIRouter(prefix="/property")

@propertiesRoutes.post("/addProperty/{userId}", response_model=Dict)
def add_propertylease(userId: str, propertyDetails: PropertyDetails) -> (int | Dict[str, Any]):
    return addProperty(userId, propertyDetails)

@propertiesRoutes.delete("/deleteProperty/{propertyId}", response_model=Dict)
def delete_lease(propertyId: int) -> Dict[str, Any]:
    return deleteProperty(propertyId)

@propertiesRoutes.get("/getProperty/{userId}", response_model=Dict)
def get_properties(property_id: int) -> (str | Dict[str, Any]):
    return getProperties(property_id)
