from alembic import context
from lifehub.core.common.base.db_model import BaseModel
from lifehub.core.common.database_service import get_engine

target_metadata = BaseModel.metadata


def run_migrations_online() -> None:
    connectable = get_engine(admin=True)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
