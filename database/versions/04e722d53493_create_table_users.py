"""create_users

Revision ID: 04e722d53493
Revises: a3bb52d4a435
Create Date: 2023-03-15 22:59:38.557942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04e722d53493'
down_revision = 'a3bb52d4a435'
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql_batch = """
    CREATE TABLE IF NOT EXISTS users (
        uuid UUID DEFAULT uuid_generate_v1() PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        deleted_at TIMESTAMPTZ
    );
    """
    op.execute(sql_batch)

def downgrade() -> None:
    pass
