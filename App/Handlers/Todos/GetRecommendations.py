from dotenv import load_dotenv
import os
import googlemaps
from App.DB.Models.Todo import Todo
from App.DB.Session import session_scope as session
from typing import Dict, Any
from sqlalchemy import select

load_dotenv()

def getRecommendations(todoId: int, propertyAddress: str) -> Dict[str, Any]:
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

        return {"data": place_details, "status_code": 200}
