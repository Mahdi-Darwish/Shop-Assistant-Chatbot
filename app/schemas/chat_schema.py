# from datetime import datetime
# from pydantic import BaseModel

# class ChatRequest(BaseModel):
#     message: str
#     conversation_id: int

# class ChatResponse(BaseModel):
#     reply: str
#     conversation_id: int

# class ChatMessageOut(BaseModel):
#     role: str
#     content: str

# class ConversationOut(BaseModel):
#     id: int
#     title: str | None
#     created_at: datetime

#     class Config:
#         from_attributes = True




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

class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: float

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
    