from fastapi import APIRouter
import pandas as pd
from dotenv import load_dotenv
import os
import googlemaps

from DB.ORM.Models.Todo import Todo
from DB.ORM.Utils.Session import session_scope as session
from typing import Union, Dict, Any
from sqlalchemy import select

router = APIRouter()
load_dotenv()


@router.get("/todo/getRecommendations/{todoId}/{propertyAddress}")
def getRecommendations(todoId: int, propertyAddress:str) -> Union[str, Dict[str, Any]]:
    with session() as db_session:
        todo_select_stmt = select(Todo).filter(Todo.todo_id == todoId)
        todo = db_session.execute(todo_select_stmt).scalars().first()

        if todo is None:
            return {"message": f"No todo found with ID {todoId}", "status_code": 404}

        gmaps = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))
        geocode_result = gmaps.geocode(propertyAddress)
        location = geocode_result[0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']

        places_result = gmaps.places_nearby(location=(latitude, longitude), radius=1500, type=str(todo.recommended_professional).lower())

        place_details = [
            {
                "name": place.get("name", "N/A"),
                "vicinity": place.get("vicinity", "N/A"),
                "rating": place.get("rating", "N/A"),
            }
            for place in places_result["results"]
        ]

        return pd.DataFrame(place_details).to_json(orient="records")



