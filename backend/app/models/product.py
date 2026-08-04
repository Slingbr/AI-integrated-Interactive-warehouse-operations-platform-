from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    sku = Column(String, unique=True, nullable=False)

    name = Column(String, nullable=False)

    quantity = Column(Integer, nullable=False)

    location_id = Column(
        Integer,
        ForeignKey("warehouse_locations.id"),
        nullable=False
    )

    location = relationship(
        "WarehouseLocation",
        back_populates="products"
    )