from typing import Dict
from fastapi import APIRouter

router = APIRouter()

@router.get("/addProperty/{userId}/{propertyDetails}")
def AddProperty(userId:str, propertyDetails:Dict[str,str]):
    print("add property")

