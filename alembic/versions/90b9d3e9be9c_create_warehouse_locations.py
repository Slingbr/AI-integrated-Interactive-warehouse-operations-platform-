"""baseline existing database schema

Revision ID: 90b9d3e9be9c
Revises:
Create Date: 2026-08-04
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "90b9d3e9be9c"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create the database schema that already exists
    in our current development database.
    """

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sku", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("aisle", sa.String(), nullable=False),
        sa.Column("shelf", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sku"),
    )

    op.create_index(
        "ix_products_id",
        "products",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Remove the baseline products table."""

    op.drop_index(
        "ix_products_id",
        table_name="products",
    )

    op.drop_table("products")