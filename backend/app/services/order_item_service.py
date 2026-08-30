from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order_item import OrderItem
from app.models.order import Order
from app.models.product import Product
from app.schemas.order_item import OrderItemCreate


def create_order_item(
    db: Session,
    order_item: OrderItemCreate
) -> OrderItem:

    # Check that the order exists
    order = (
        db.query(Order)
        .filter(Order.id == order_item.order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # Check that the product exists
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

    # Check requested quantity is valid
    if order_item.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    # Check enough stock exists
    if order_item.quantity > product.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient product stock"
        )

    new_order_item = OrderItem(
        order_id=order_item.order_id,
        product_id=order_item.product_id,
        quantity=order_item.quantity,
        picked_quantity=0
    )

    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)

    return new_order_item