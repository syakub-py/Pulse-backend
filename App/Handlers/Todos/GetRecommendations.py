from dotenv import load_dotenv
import os
import googlemaps
from App.DB.Models.Todo import Todo
from App.DB.Session import session_scope as session
from typing import Dict, Any
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from googlemaps.exceptions import ApiError

load_dotenv()

def getRecommendations(todoId: int, propertyAddress: str) -> Dict[str, Any]:
    try:
        with session() as db_session:
            todo_select_stmt = select(Todo).filter(Todo.todo_id == todoId)
            todo = db_session.execute(todo_select_stmt).scalars().first()

            if todo is None:
                return {"message": f"No todo found with ID {todoId}", "status_code": 404}

            gmaps = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))

            geocode_result = gmaps.geocode(propertyAddress)
            if not geocode_result:
                return {"message": f"Invalid address: {propertyAddress}", "status_code": 400}

            location = geocode_result[0]['geometry']['location']
            latitude, longitude = location['lat'], location['lng']

            places_result = gmaps.places_nearby(location=(latitude, longitude), radius=1500, type=str(todo.recommended_professional).lower())

            place_details = [
                {
                    "name": place.get("name", "N/A"),
                    "vicinity": place.get("vicinity", "N/A"),
                    "rating": place.get("rating", "N/A"),
                }
                for place in places_result.get("results", [])
            ]

            return {"data": place_details, "status_code": 200}

    except SQLAlchemyError as db_error:
        return {"message": "Database error occurred.", "error": str(db_error), "status_code": 500}
    except ApiError as api_error:
        return {"message": "Google Maps API error occurred.", "error": str(api_error), "status_code": 500}
    except Exception as e:
        return {"message": "An unexpected error occurred.", "error": str(e), "status_code": 500}
