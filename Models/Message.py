from pydantic import BaseModel

class Message(BaseModel):
    user_id: int
    role: str
    message: str
    created_at: str
