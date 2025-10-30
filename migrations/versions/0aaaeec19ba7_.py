"""set default disc to 1

Revision ID: 0aaaeec19ba7
Revises: 20252200d08d
Create Date: 2025-10-30 12:22:36.828340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0aaaeec19ba7'
down_revision = '20252200d08d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('saves', schema=None) as batch_op:
        batch_op.alter_column(
            'disc',
            existing_type=sa.Integer(),
            server_default=sa.text('1'),
            existing_nullable=False
        )


def downgrade():
    with op.batch_alter_table('saves', schema=None) as batch_op:
        batch_op.alter_column(
            'disc',
            existing_type=sa.Integer(),
            server_default=sa.text('0'),
            existing_nullable=False
        )
