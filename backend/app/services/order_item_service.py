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

    # Check order exists
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

    # Check product exists
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

    # Validate quantity
    if order_item.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    # Check stock
    if order_item.quantity > product.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient product stock"
        )

    existing_order_item.order_id = order_item.order_id
    existing_order_item.product_id = order_item.product_id
    existing_order_item.quantity = order_item.quantity

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