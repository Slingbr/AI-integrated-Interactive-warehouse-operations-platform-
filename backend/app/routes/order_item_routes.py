from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.order_item import OrderItem
from app.schemas.order_item import OrderItemCreate, OrderItemResponse
from app.services import order_item_service

router = APIRouter()


@router.post(
    "/order-items",
    response_model=OrderItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order_item(
    order_item: OrderItemCreate,
    db: Session = Depends(get_db)
):
    return order_item_service.create_order_item(db, order_item)


@router.get(
    "/order-items",
    response_model=list[OrderItemResponse]
)
def get_order_items(
    db: Session = Depends(get_db)
):
    return order_item_service.get_order_items(db)


@router.get(
    "/order-items/{order_item_id}",
    response_model=OrderItemResponse
)
def get_order_item(
    order_item_id: int,
    db: Session = Depends(get_db)
):
    return order_item_service.get_order_item(db, order_item_id)


@router.put(
    "/order-items/{order_item_id}",
    response_model=OrderItemResponse
)
def update_order_item(
    order_item_id: int,
    order_item: OrderItemCreate,
    db: Session = Depends(get_db)
):
    return order_item_service.update_order_item(
        db,
        order_item_id,
        order_item
    )


@router.delete(
    "/order-items/{order_item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_order_item(
    order_item_id: int,
    db: Session = Depends(get_db)
):
    order_item_service.delete_order_item(db, order_item_id)