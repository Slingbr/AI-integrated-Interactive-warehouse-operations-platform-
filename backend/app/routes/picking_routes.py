from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.picking import PickRequest
from app.services import picking_service


router = APIRouter(
    prefix="/picking",
    tags=["Picking"]
)


@router.post("/order-items/{order_item_id}")
def pick_order_item(
    order_item_id: int,
    pick_request: PickRequest,
    db: Session = Depends(get_db)
):
    return picking_service.pick_order_item(
        db,
        order_item_id,
        pick_request.worker_id,
        pick_request.quantity
    )