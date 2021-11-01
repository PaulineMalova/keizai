from __future__ import with_statement

import os
import sys
import sqlalchemy_utils

from alembic import context
from sqlalchemy import engine_from_config, pool, MetaData
from logging.config import fileConfig

from app import settings
from app.user.models import User

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# this will overwrite the ini-file sqlalchemy.url path
# with the path given in the config of the main code

current_dir = os.path.dirname(os.path.realpath(__file__))
target_dir = os.path.join(current_dir, "..", "..")
sys.path.insert(0, target_dir)


db_string = "{0}://{1}:{2}@{3}/{4}".format(
    settings.DATABASE["drivername"],
    settings.DATABASE["username"],
    settings.DATABASE["password"],
    settings.DATABASE["host"],
    settings.DATABASE["database"],
)

config.set_main_option("sqlalchemy.url", db_string)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)


def combine_metadata(*args):
    m = MetaData()
    for metadata in args:
        for t in metadata.tables.values():
            t.tometadata(m)
    return m


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = combine_metadata(
    # user
    User.metadata
)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def render_item(type_, obj, autogen_context):
    """Apply custom rendering for selected items."""

    if type_ == "type" and isinstance(
        obj, sqlalchemy_utils.types.uuid.UUIDType
    ):
        # add import for this type
        autogen_context.imports.add("import sqlalchemy_utils")
        autogen_context.imports.add("import uuid")
        return "sqlalchemy_utils.types.uuid.UUIDType(), default=uuid.uuid4"

    # default rendering for other objects
    return False


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    alembic_config = config.get_section(config.config_ini_section)
    alembic_config["sqlalchemy.url"] = db_string

    connectable = engine_from_config(
        alembic_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
