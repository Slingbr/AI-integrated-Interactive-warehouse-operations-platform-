from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.worker import Worker


def pick_order_item(
    db: Session,
    order_item_id: int,
    worker_id: int,
    quantity: int
) -> OrderItem:

    # Find the order item
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

    # Find the worker
    worker = (
        db.query(Worker)
        .filter(Worker.id == worker_id)
        .first()
    )

    if worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker not found"
        )

    # Validate quantity
    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Pick quantity must be greater than 0"
        )

    # Make sure we don't pick more than ordered
    remaining_quantity = (
        order_item.quantity - order_item.picked_quantity
    )

    if quantity > remaining_quantity:
        raise HTTPException(
            status_code=400,
            detail="Cannot pick more than the remaining quantity"
        )

    # Find the product
    product = (
        db.query(Product)
        .filter(Product.id == order_item.product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Make sure there is enough stock
    if quantity > product.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient product stock"
        )

    # Perform the pick
    order_item.picked_quantity += quantity
    product.quantity -= quantity

    db.commit()
    db.refresh(order_item)

    # Check whether the entire order has now been picked
    order = (
        db.query(Order)
        .filter(Order.id == order_item.order_id)
        .first()
    )

    if order is not None:

        order_items = (
            db.query(OrderItem)
            .filter(OrderItem.order_id == order.id)
            .all()
        )

        all_picked = all(
            item.picked_quantity >= item.quantity
            for item in order_items
        )

        if all_picked:
            order.status = "COMPLETED"
            db.commit()

    return order_item