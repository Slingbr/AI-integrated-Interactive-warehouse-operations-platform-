from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services import order_service

router = APIRouter()


@router.post(
    "/orders",
    response_model=OrderResponse
)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    return order_service.create_order(db, order)


@router.get(
    "/orders",
    response_model=list[OrderResponse]
)
def get_orders(
    db: Session = Depends(get_db)
):
    return order_service.get_orders(db)


@router.get(
    "/orders/{order_number}",
    response_model=OrderResponse
)
def get_order(
    order_number: str,
    db: Session = Depends(get_db)
):
    return order_service.get_order(
        db,
        order_number
    )


@router.put(
    "/orders/{order_id}",
    response_model=OrderResponse
)
def update_order(
    order_id: int,
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    return order_service.update_order(
        db,
        order_id,
        order
    )


@router.delete(
    "/orders/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order_service.delete_order(
        db,
        order_id
    )