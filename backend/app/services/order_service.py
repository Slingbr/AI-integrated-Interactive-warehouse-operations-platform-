from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.order import Order
from app.models.worker import Worker
from app.schemas.order import OrderCreate


def create_order(
    db: Session,
    order: OrderCreate
) -> Order:

    if order.assigned_worker_id is not None:
        worker = (
            db.query(Worker)
            .filter(Worker.id == order.assigned_worker_id)
            .first()
        )

        if worker is None:
            raise HTTPException(
                status_code=400,
                detail="Assigned worker does not exist"
            )

    new_order = Order(
        order_number=order.order_number,
        status=order.status,
        priority=order.priority,
        assigned_worker_id=order.assigned_worker_id
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


def get_orders(
    db: Session
) -> list[Order]:

    return db.query(Order).all()


def get_order(
    db: Session,
    order_number: str
) -> Order:

    order = (
        db.query(Order)
        .filter(Order.order_number == order_number)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


def update_order(
    db: Session,
    order_id: int,
    order: OrderCreate
) -> Order:

    existing_order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if existing_order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.assigned_worker_id is not None:
        worker = (
            db.query(Worker)
            .filter(Worker.id == order.assigned_worker_id)
            .first()
        )

        if worker is None:
            raise HTTPException(
                status_code=400,
                detail="Assigned worker does not exist"
            )

    for key, value in order.model_dump().items():
        setattr(existing_order, key, value)

    db.commit()
    db.refresh(existing_order)

    return existing_order


def delete_order(
    db: Session,
    order_id: int
) -> None:

    existing_order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if existing_order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db.delete(existing_order)
    db.commit()