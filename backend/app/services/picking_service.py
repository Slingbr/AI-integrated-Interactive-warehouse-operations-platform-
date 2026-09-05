from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem


def pick_order_item(
    db: Session,
    order_item_id: int,
    quantity_to_pick: int
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

    if quantity_to_pick <= 0:
        raise HTTPException(
            status_code=400,
            detail="Pick quantity must be greater than 0"
        )

    new_picked_quantity = (
        order_item.picked_quantity + quantity_to_pick
    )

    if new_picked_quantity > order_item.quantity:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Cannot pick {quantity_to_pick} items. "
                f"Only {order_item.quantity - order_item.picked_quantity} remaining."
            )
        )

    order_item.picked_quantity = new_picked_quantity

    order = (
        db.query(Order)
        .filter(Order.id == order_item.order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Parent order not found"
        )


    if order.status == "PENDING":
        order.status = "PICKING"

   
    order_items = (
        db.query(OrderItem)
        .filter(OrderItem.order_id == order.id)
        .all()
    )

    all_items_picked = all(
        item.picked_quantity >= item.quantity
        for item in order_items
    )

   
    if all_items_picked:
        order.status = "READY_FOR_PACKING"

    db.commit()
    db.refresh(order_item)

    return order_item