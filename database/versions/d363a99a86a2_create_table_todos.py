"""create_table_todos

Revision ID: d363a99a86a2
Revises: 04e722d53493
Create Date: 2023-03-15 23:02:29.341537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd363a99a86a2'
down_revision = '04e722d53493'
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql_batch = """
    CREATE TABLE IF NOT EXISTS todos (
        uuid UUID DEFAULT uuid_generate_v1() PRIMARY KEY,
        user_uuid UUID NOT NULL,
        name VARCHAR(255) NOT NULL,
        done BOOLEAN DEFAULT FALSE,
        due_to TIMESTAMPTZ,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        deleted_at TIMESTAMPTZ
    );

    ALTER TABLE todos
    ADD CONSTRAINT fk_users_todos
    FOREIGN KEY (user_uuid)
    REFERENCES users (uuid);
    """
    op.execute(sql_batch)


def downgrade() -> None:
    pass
