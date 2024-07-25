from fastapi import APIRouter, HTTPException, status
from DB.ORM.Models import Property
from DB.ORM.Utils.Session import session

router = APIRouter()

@router.delete("/deleteProperty/{propertyId}")
def deleteProperty(propertyId: int):
    try:
        property_to_delete = session.query(Property).filter(Property.property_id == propertyId).first()
        if property_to_delete:
            session.delete(property_to_delete)
            session.commit()
            return {"message": "Property deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete property") from e


