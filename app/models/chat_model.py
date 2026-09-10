from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship
from app.database import Base
class ChatConversation(Base):
    """One row per distinct chat thread — this is what powers the
    sidebar list, same idea as Claude's own conversation list."""
    __tablename__ = "chat_conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    messages = relationship(
        "ChatMessage", back_populates="conversation", cascade="all, delete-orphan"
    )

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(
        Integer, ForeignKey("chat_conversations.id"), nullable=False, index=True
    )
    role = Column(String, nullable=False)  # "user" | "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    conversation = relationship("ChatConversation", back_populates="messages")