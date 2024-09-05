from typing import Dict
from fastapi import APIRouter
from Models.PropertyDetails import PropertyDetails
from App.Handlers.Properties.AddProperty import addProperty
from App.Handlers.Properties.DeleteProperty import deleteProperty
from App.Handlers.Properties.GetProperties import getProperties

propertiesRoutes = APIRouter(prefix="/property")

@propertiesRoutes.post("/addProperty/{userId}", response_model=Dict)
async def add_propertylease(userId: str, propertyDetails: PropertyDetails):
    return addProperty(userId, propertyDetails)

@propertiesRoutes.delete("/deleteProperty/{propertyId}", response_model=Dict)
async def delete_lease(propertyId: int):
    return deleteProperty(propertyId)

@propertiesRoutes.get("/getProperty/{userId}", response_model=Dict)
async def get_properties(property_id: int):
    return getProperties(property_id)
