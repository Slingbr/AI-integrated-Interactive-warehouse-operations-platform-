from logging.config import fileConfig
from pathlib import Path
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from dotenv import load_dotenv

from alembic import context


# ---------------------------------------------------------
# Make the backend folder available to Python imports
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"

sys.path.insert(0, str(BACKEND_DIR))


# ---------------------------------------------------------
# Load environment variables from backend/.env
# ---------------------------------------------------------

load_dotenv(BACKEND_DIR / ".env")


# ---------------------------------------------------------
# Import our SQLAlchemy database configuration
# and models
# ---------------------------------------------------------

from app.database.connection import Base, DATABASE_URL
from app.models.product import Product
from app.models.warehouse_location import WarehouseLocation


# ---------------------------------------------------------
# Alembic configuration
# ---------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Tell Alembic which database to connect to
config.set_main_option(
    "sqlalchemy.url",
    DATABASE_URL.replace("%", "%%")
)

# Tell Alembic about our SQLAlchemy models
target_metadata = Base.metadata


# ---------------------------------------------------------
# Offline migrations
# ---------------------------------------------------------

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------
# Online migrations
# ---------------------------------------------------------

def run_migrations_online() -> None:

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

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