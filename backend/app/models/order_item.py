from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.connection import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    picked_quantity = Column(
        Integer,
        nullable=False,
        default=0
    )

    order = relationship(
        "Order",
        back_populates="items"
    )

    product = relationship("Product")