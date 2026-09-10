from sqlalchemy.orm import Session
from sqlalchemy import Select
from sqlalchemy import select
from app.core.security import hash_password
from app.models.cart_model import Cart, CartItem
from app.models.chat_model import ChatConversation, ChatMessage
from app.models.order_model import Order
from app.models.user_model import User

def get_user_by_username(db:Session,username:str) ->User|None:
    statement = select(User).where(User.username == username)
    return db.scalars(statement).first()

def get_user_by_id(db:Session,user_id:int) ->User|None:
    statement = select(User).where(User.id == user_id)
    return db.scalars(statement).first()

def create_user(db:Session,username:str,password:str,phone:str) ->User:
    new_user = User(username=username,hashed_password=hash_password(password),phone=phone,role="customer")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
def all_users(db:Session) ->list[User]:
    statement = select(User)
    return db.scalars(statement).all()
def set_user_active_status(db:Session,user_id:int,is_active:bool) -> User | None:
    user = get_user_by_id(db,user_id)
    if not user:
        return None
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> tuple[bool, str]:
    """Hard delete — permanently removes the account. Returns
    (success, message). Refuses to delete any user with real order
    history, since that would corrupt those orders' records; the admin
    should deactivate that user instead. Safe to delete carts and chat
    conversations first since those carry no independent business value
    once the user is gone."""
    user = get_user_by_id(db, user_id)
    if not user:
        return False, "User not found."
 
    has_orders = db.scalar(select(Order.id).where(Order.user_id == user_id).limit(1))
    if has_orders:
        return False, "This user has order history and cannot be deleted — deactivate instead."
 
    cart_ids = db.scalars(select(Cart.id).where(Cart.user_id == user_id)).all()
    if cart_ids:
        db.query(CartItem).filter(CartItem.cart_id.in_(cart_ids)).delete(synchronize_session=False)
        db.query(Cart).filter(Cart.user_id == user_id).delete(synchronize_session=False)
 
    conversation_ids = db.scalars(
        select(ChatConversation.id).where(ChatConversation.user_id == user_id)
    ).all()
    if conversation_ids:
        db.query(ChatMessage).filter(
            ChatMessage.conversation_id.in_(conversation_ids)
        ).delete(synchronize_session=False)
        db.query(ChatConversation).filter(ChatConversation.user_id == user_id).delete(
            synchronize_session=False
        )
    db.delete(user)
    db.commit()
    return True, "User deleted."
def search_users_by_username(db:Session,user_name:str) ->list[User]:
    statement = select(User).where(User.username.ilike(f"%{user_name}%"))
    return db.scalars(statement).all()
# this function is used to flips the role field for users, role must be admin or customer the route layer validates this not the caller
def set_user_role(db: Session, user_id: int, role: str) -> User | None:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    user.role = role
    db.commit()
    db.refresh(user)
    return user
