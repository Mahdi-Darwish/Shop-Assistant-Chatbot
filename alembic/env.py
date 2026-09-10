from logging.config import fileConfig
from alembic import context
from app.database import Base, engine
# Import all models so SQLAlchemy knows about them
from app.models.product_model import Product
from app.models.user_model import User
from app.models.cart_model import Cart,CartItem
from app.models.order_model import Order,OrderItem
from app.models.chat_model import ChatMessage


from app.services.products_services import Product
# from app.models.user_model import User


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    url = str(engine.url)

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()