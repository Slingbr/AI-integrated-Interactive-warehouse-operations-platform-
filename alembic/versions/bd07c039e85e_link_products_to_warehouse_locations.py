"""link products to warehouse locations

Revision ID: bd07c039e85e
Revises: 90b9d3e9be9c
Create Date: 2026-08-13
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


#revision 
revision: str = "bd07c039e85e"
down_revision: Union[str, Sequence[str], None] = "90b9d3e9be9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    # Creating warehouse locations
    

    op.create_table(
        "warehouse_locations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("location_type", sa.String(), nullable=False),
        sa.Column("x_coordinate", sa.Integer(), nullable=False),
        sa.Column("y_coordinate", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )

    op.create_index(
        "ix_warehouse_locations_id",
        "warehouse_locations",
        ["id"],
        unique=False,
    )

   

    op.add_column(
        "products",
        sa.Column("location_id", sa.Integer(), nullable=True),
    )

   

    op.execute(
        """
        INSERT INTO warehouse_locations
            (code, name, location_type, x_coordinate, y_coordinate)
        VALUES
            ('A-12', 'Shelf A12', 'shelf', 1, 12),
            ('B-5', 'Shelf B5', 'shelf', 2, 5)
        """
    )

    
    #Assigned existing products to their new locations
    op.execute(
        """
        UPDATE products
        SET location_id = warehouse_locations.id
        FROM warehouse_locations
        WHERE warehouse_locations.code =
            products.aisle || '-' || products.shelf
        """
    )


    connection = op.get_bind()

    missing_locations = connection.execute(
        sa.text(
            """
            SELECT COUNT(*)
            FROM products
            WHERE location_id IS NULL
            """
        )
    ).scalar()

    if missing_locations:
        raise RuntimeError(
            f"{missing_locations} product(s) could not be assigned "
            "to a warehouse location."
        )


    op.alter_column(
        "products",
        "location_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

  
    #Added the foreign key
  
    op.create_foreign_key(
        "fk_products_location_id",
        "products",
        "warehouse_locations",
        ["location_id"],
        ["id"],
    )


    op.drop_column("products", "shelf")
    op.drop_column("products", "aisle")


def downgrade() -> None:

    op.add_column(
        "products",
        sa.Column("aisle", sa.String(), nullable=True),
    )

    op.add_column(
        "products",
        sa.Column("shelf", sa.String(), nullable=True),
    )


    op.execute(
        """
        UPDATE products
        SET
            aisle = split_part(warehouse_locations.code, '-', 1),
            shelf = split_part(warehouse_locations.code, '-', 2)
        FROM warehouse_locations
        WHERE products.location_id = warehouse_locations.id
        """
    )


    op.alter_column(
        "products",
        "aisle",
        existing_type=sa.String(),
        nullable=False,
    )

    op.alter_column(
        "products",
        "shelf",
        existing_type=sa.String(),
        nullable=False,
    )


    op.drop_constraint(
        "fk_products_location_id",
        "products",
        type_="foreignkey",
    )


    op.drop_column("products", "location_id")


    op.drop_index(
        "ix_warehouse_locations_id",
        table_name="warehouse_locations",
    )

    op.drop_table("warehouse_locations")