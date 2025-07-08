"""empty message

Revision ID: 821e0fa19ffb
Revises: a3fcc928a679
Create Date: 2025-06-27 23:09:39.144617

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "821e0fa19ffb"
down_revision = "a3fcc928a679"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("party", schema=None) as batch_op:
        batch_op.alter_column(
            "name", existing_type=sa.String(length=80), nullable=False
        )

        # batch_op.drop_constraint("name", type_="unique")

        batch_op.create_unique_constraint(
            "uix_saveid_name",  # Constraint name
            ["save_id", "name"],  # Columns
        )


def downgrade():
    with op.batch_alter_table("party", schema=None) as batch_op:
        batch_op.alter_column("name", existing_type=sa.String(length=80), nullable=True)
        batch_op.drop_constraint("uix_saveid_name", type_="unique")