from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order_item import OrderItem
from app.schemas.order_item import OrderItemCreate


def create_order_item(
    db: Session,
    order_item: OrderItemCreate
) -> OrderItem:

    new_order_item = OrderItem(
        order_id=order_item.order_id,
        product_id=order_item.product_id,
        quantity=order_item.quantity,
        picked_quantity=order_item.picked_quantity
    )

    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)

    return new_order_item


def get_order_items(
    db: Session
) -> list[OrderItem]:

    return db.query(OrderItem).all()


def get_order_item(
    db: Session,
    order_item_id: int
) -> OrderItem:

    order_item = (
        db.query(OrderItem)
        .filter(OrderItem.id == order_item_id)
        .first()
    )

    if order_item is None:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    return order_item


def update_order_item(
    db: Session,
    order_item_id: int,
    order_item: OrderItemCreate
) -> OrderItem:

    existing_order_item = (
        db.query(OrderItem)
        .filter(OrderItem.id == order_item_id)
        .first()
    )

    if existing_order_item is None:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    for key, value in order_item.model_dump().items():
        setattr(existing_order_item, key, value)

    db.commit()
    db.refresh(existing_order_item)

    return existing_order_item


def delete_order_item(
    db: Session,
    order_item_id: int
) -> None:

    existing_order_item = (
        db.query(OrderItem)
        .filter(OrderItem.id == order_item_id)
        .first()
    )

    if existing_order_item is None:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    db.delete(existing_order_item)
    db.commit()