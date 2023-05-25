"""create extensions

Revision ID: a3bb52d4a435
Revises: 
Create Date: 2023-03-15 22:52:07.384923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a3bb52d4a435"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql_batch = """
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    """
    op.execute(sql_batch)


def downgrade() -> None:
    pass
