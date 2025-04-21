"""add is_admin to user

Revision ID: d9a8c1b0274f
Revises:
Create Date: 2025-04-21 13:42:40.060067

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import Boolean, String
from sqlalchemy.sql import column, table

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d9a8c1b0274f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add the is_admin column
    op.add_column(
        "user",
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    user = table(
        "user",
        column("username", String),
        column("is_admin", Boolean),
    )
    # Give admin privileges to the admin user
    op.execute(user.update().where(user.c.username == "admin").values(is_admin=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user", "is_admin")
