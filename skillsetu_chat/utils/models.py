from datetime import datetime
from typing import Literal, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class FileData(BaseModel):
    name: str
    type: str
    url: str


class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    sender: Optional[str] = None
    receiver: str
    status: Literal["sent", "delivered", "read"] = "sent"
    message: str
    attachments: Optional[list[str]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChatMessage(BaseModel):
    messages: list[Message]
    users: list[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
