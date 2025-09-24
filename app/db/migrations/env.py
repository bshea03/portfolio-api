from logging.config import fileConfig
from dotenv import load_dotenv
import os
import sys

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from app.models.award import Award
from app.models.job import Job
from app.models.project import Project
from app.models.skill import Skill

from alembic import context

# Set target metadata for autogeneration
from app.database import Base
target_metadata = Base.metadata

# Load environment variables from the correct .env file
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
env_file_name = os.getenv("ENV_FILE", ".env.dev")
env_file_path = os.path.join(project_root, env_file_name)
load_dotenv(env_file_path)

# Read DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL is not set. Check your .env file and container environment.")

# Inject DATABASE_URL into Alembic config
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
