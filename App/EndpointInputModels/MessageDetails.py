from pydantic import BaseModel, Field
from typing import Optional
import random
import datetime

class User(BaseModel):
    id: int = Field(alias="_id")
    name: str
    avatar: Optional[str] = None

class MessageDetails(BaseModel):
    id: int = Field(default_factory=lambda: random.randint(1, 100000), alias="_id")
    text: str
    createdAt: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    user: User

