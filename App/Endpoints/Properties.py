from typing import Dict, Any
from fastapi import APIRouter
from App.EndpointInputModels.PropertyDetails import PropertyDetails
from App.Handlers.Properties.AddProperty import addProperty
from App.Handlers.Properties.DeleteProperty import deleteProperty
from App.Handlers.Properties.GetProperties import getProperties

propertiesRoutes = APIRouter(prefix="/property")

@propertiesRoutes.post("/addProperty/{postgresUserId}/{firebaseUserId}", response_model=Dict)
def add_property(postgresUserId:int, firebaseUserId: str, propertyDetails: PropertyDetails) -> Dict[str, Any]:
    return addProperty(postgresUserId, firebaseUserId, propertyDetails)

@propertiesRoutes.delete("/deleteProperty/{propertyId}", response_model=Dict)
def delete_property(propertyId: int) -> Dict[str, Any]:
    return deleteProperty(propertyId)

@propertiesRoutes.get("/getProperty/{userId}", response_model=Dict)
def get_property(userId: int) -> Dict[str, Any]:
    return getProperties(userId)
