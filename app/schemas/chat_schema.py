from datetime import datetime
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    conversation_id: int
    # Only honoured by the admin chat: an image the admin already uploaded
    # through POST /admin/uploads/product-image.
    image_url: str | None = None

class ChatResponse(BaseModel):
    reply: str
    conversation_id: int
    cards: dict | None = None
    image_used: bool = False

class ChatMessageOut(BaseModel):
    role: str
    content: str
    cards: dict | None = None

class ConversationOut(BaseModel):
    id: int
    title: str | None
    created_at: datetime

    class Config:
        from_attributes = True

class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    image_url: str | None = None

    class Config:
        from_attributes = True

class GuestChatMessage(BaseModel):
    role: str
    content: str

class GuestChatRequest(BaseModel):
    message: str
    history: list[GuestChatMessage] = []

class GuestChatResponse(BaseModel):
    reply: str
    cards: dict | None = None
    