from datetime import datetime

from App.LoggerConfig import pulse_logger as logger
from App.DB.Session import session_scope as session
from App.DB.Models.Todo import Todo
import ollama
from dotenv import load_dotenv
import os
from typing import Dict, Any
from ollama import Message

from App.Models.TodoDetails import TodoDetails

load_dotenv()
place_types = [
    "accounting",
    "airport",
    "amusement_park",
    "aquarium",
    "art_gallery",
    "atm",
    "bakery",
    "bank",
    "bar",
    "beauty_salon",
    "bicycle_store",
    "book_store",
    "bowling_alley",
    "bus_station",
    "cafe",
    "campground",
    "car_dealer",
    "car_rental",
    "car_repair",
    "car_wash",
    "casino",
    "cemetery",
    "church",
    "city_hall",
    "clothing_store",
    "convenience_store",
    "courthouse",
    "dentist",
    "department_store",
    "doctor",
    "drugstore",
    "electrician",
    "electronics_store",
    "embassy",
    "fire_station",
    "florist",
    "funeral_home",
    "furniture_store",
    "gas_station",
    "gym",
    "hair_care",
    "hardware_store",
    "hindu_temple",
    "home_goods_store",
    "hospital",
    "insurance_agency",
    "jewelry_store",
    "laundry",
    "lawyer",
    "library",
    "light_rail_station",
    "liquor_store",
    "local_government_office",
    "locksmith",
    "lodging",
    "meal_delivery",
    "meal_takeaway",
    "mosque",
    "movie_rental",
    "movie_theater",
    "moving_company",
    "museum",
    "night_club",
    "painter",
    "park",
    "parking",
    "pet_store",
    "pharmacy",
    "physiotherapist",
    "plumber",
    "police",
    "post_office",
    "primary_school",
    "real_estate_agency",
    "restaurant",
    "roofing_contractor",
    "rv_park",
    "school",
    "secondary_school",
    "shoe_store",
    "shopping_mall",
    "spa",
    "stadium",
    "storage",
    "store",
    "subway_station",
    "supermarket",
    "synagogue",
    "taxi_stand",
    "tourist_attraction",
    "train_station",
    "transit_station",
    "travel_agency",
    "university",
    "veterinary_care",
    "zoo"
]

def addTodo(todo: TodoDetails) -> (int | Dict[str, Any]):
    if not todo:
        return {"message": "no todo details were provided", "status_code": 500}
    try:
        with session() as db_session:
            logger.info("Adding Todo to property id: {}".format(todo.PropertyId))

            system_prompt = Message(role="system", content="""You are an expert assistant specializing in recommending professionals to resolve property management issues. When the user provides a description of a problem, your task is to identify the most appropriate type of professional or service provider to address the issue. Your response should always consist of just the professional's title, without any additional information.""")
            user_message = Message(role="user", content=todo.Description)
            messages_list = [system_prompt, user_message]

            model=os.getenv("CHAT_MODEL")
            if model is None:
                return {"message": "model not found", "status_code": 500}
            aiResponse = ollama.chat(model, messages=messages_list)
            professional = aiResponse['message']['content']

            new_todo = Todo(
                property_id=todo.PropertyId,
                title=todo.Title,
                description=todo.Description,
                status=todo.Status,
                priority=todo.Priority,
                added_by=todo.AddedBy,
                recommended_professional=str(professional).replace(" ", "_"),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            db_session.add(new_todo)
            db_session.commit()

            db_session.refresh(new_todo)

            return int(new_todo.todo_id)
    except Exception as e:
        logger.error("Error adding the todo: {}".format(e))
        db_session.rollback()
        return {"message": str(e), "status_code": 500}
    finally:
        db_session.close()
