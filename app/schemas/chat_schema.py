from datetime import datetime
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    conversation_id: int

class ChatResponse(BaseModel):
    reply: str
    conversation_id: int

class ChatMessageOut(BaseModel):
    role: str
    content: str

class ConversationOut(BaseModel):
    id: int
    title: str | None
    created_at: datetime

    class Config:
        from_attributes = True