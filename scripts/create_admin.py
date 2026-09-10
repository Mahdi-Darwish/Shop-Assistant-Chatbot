import getpass
from app.core.security import hash_password
from app.database import SessionLocal
from app.models.user_model import User
from app.services.user_services import get_user_by_username
from app.models.product_model import Product


def create_admin():
    db = SessionLocal()
    try:
        username = input("Admin username: ").strip()

        if get_user_by_username(db, username):
            print(f"Error: a user named '{username}' already exists.")
            print("If you want to promote an EXISTING user instead, use the")
            print("PATCH /admin/users/{id}/promote endpoint via another admin.")
            return

        password = getpass.getpass("Admin password: ")
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Error: passwords don't match.")
            return

        phone = input("Phone number: ").strip()

        admin_user = User(
            username=username,
            hashed_password=hash_password(password),
            phone=phone,
            role="admin",
            is_active=True,
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"\nAdmin account created: '{admin_user.username}' (id={admin_user.id})")
        print("You can now log in through the normal /login endpoint.")
    finally:
        db.close()
if __name__ == "__main__":
    create_admin()