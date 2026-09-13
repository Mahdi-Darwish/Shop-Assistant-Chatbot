from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.chat_model import ChatConversation, ChatMessage

HISTORY_LIMIT = 20
def create_conversation(db: Session, user_id: int) -> ChatConversation:
    conversation = ChatConversation(user_id=user_id, title=None)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation
def get_conversations_by_user(db: Session, user_id: int) -> list[ChatConversation]:
    """Newest first — matches how a sidebar list is normally read."""
    statement = (
        select(ChatConversation)
        .where(ChatConversation.user_id == user_id)
        .order_by(ChatConversation.created_at.desc())
    )
    return db.scalars(statement).all()
def get_conversation(db: Session, user_id: int, conversation_id: int) -> ChatConversation | None:
    """Scoped by BOTH id and user_id in the same query — a user can never
    open someone else's conversation by guessing its id."""
    statement = select(ChatConversation).where(
        ChatConversation.id == conversation_id, ChatConversation.user_id == user_id
    )
    return db.scalars(statement).first()
def get_messages_for_conversation(db: Session, conversation_id: int) -> list[ChatMessage]:
    """Caller is responsible for having already verified ownership via
    get_conversation() first — this function trusts conversation_id is
    already confirmed to belong to the right user."""
    statement = (
        select(ChatMessage)
        .where(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(HISTORY_LIMIT)
    )
    messages = db.scalars(statement).all()
    return list(reversed(messages))
def save_message(db: Session, conversation_id: int, role: str, content: str) -> ChatMessage:
    message = ChatMessage(conversation_id=conversation_id, role=role, content=content)
    db.add(message)
    if role == "user":
        conversation = db.get(ChatConversation, conversation_id)
        if conversation and conversation.title is None:
            conversation.title = content[:50]
    db.commit()
    db.refresh(message)
    return message