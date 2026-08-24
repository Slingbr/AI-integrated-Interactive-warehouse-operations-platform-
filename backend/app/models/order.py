from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    order_number = Column(
        String,
        unique=True,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    priority = Column(
        String,
        nullable=False
    )

    assigned_worker_id = Column(
        Integer,
        ForeignKey("workers.id"),
        nullable=True
    )

    assigned_worker = relationship("Worker")

    items = relationship(
        "OrderItem",
        back_populates="order"
    )