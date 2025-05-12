"""hash user emails

Revision ID: 2628905c520c
Revises: d9a8c1b0274f
Create Date: 2025-04-21 23:47:49.722963

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from alembic import op
from lifehub.config.constants import cfg
from lifehub.core.security.encryption import EncryptionService
from lifehub.core.user.schema import User

# revision identifiers, used by Alembic.
revision: str = "2628905c520c"
down_revision: Union[str, None] = "d9a8c1b0274f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add email_hash column
    with op.get_context().autocommit_block():
        conn = op.get_bind()
        insp = sa.inspect(conn)
        if not insp.has_table("user") or "email_hash" not in [
            col["name"] for col in insp.get_columns("user")
        ]:
            op.add_column(
                "user",
                sa.Column("email_hash", sa.String(64), nullable=True, unique=True),
            )

            # Get a database connection and create a session
            connection = op.get_bind()
            Session = sessionmaker(bind=connection)
            session = Session()

            try:
                # Update email_hash for all users
                for user in session.query(User).all():
                    encryption_service = EncryptionService(session, user)
                    email = encryption_service.decrypt_data(user.email)
                    email_hash = EncryptionService.hmac(
                        email.lower(), cfg.EMAIL_SECRET_KEY
                    )

                    user.email_hash = email_hash
                    session.commit()

                # Make email_hash non-nullable
                op.alter_column(
                    "user", "email_hash", existing_type=sa.String(64), nullable=False
                )

            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user", "email_hash")
