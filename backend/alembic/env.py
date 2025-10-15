from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from alembic import context
import os

from src.infrastructure.db import Base, DATABASE_URL  # type: ignore
from src.infrastructure import models  # noqa: F401

config = context.config
if config.get_main_option("sqlalchemy.url") == "":
    config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", DATABASE_URL))

fileConfig(config.config_file_name) if config.config_file_name else None

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
