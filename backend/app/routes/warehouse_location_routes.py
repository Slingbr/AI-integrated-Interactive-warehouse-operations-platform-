from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.warehouse_location import (
    WarehouseLocationCreate,
    WarehouseLocationResponse
)
from app.services import warehouse_location_service

router = APIRouter()


@router.post(
    "/warehouse-locations",
    response_model=WarehouseLocationResponse
)
def create_warehouse_location(
    warehouse_location: WarehouseLocationCreate,
    db: Session = Depends(get_db)
):
    return warehouse_location_service.create_location(
        db,
        warehouse_location
    )


@router.get(
    "/warehouse-locations",
    response_model=list[WarehouseLocationResponse]
)
def get_warehouse_locations(
    db: Session = Depends(get_db)
):
    return warehouse_location_service.get_locations(db)


@router.get(
    "/warehouse-locations/{warehouse_location_id}",
    response_model=WarehouseLocationResponse
)
def get_warehouse_location(
    warehouse_location_id: int,
    db: Session = Depends(get_db)
):
    return warehouse_location_service.get_location(
        db,
        warehouse_location_id
    )


@router.put(
    "/warehouse-locations/{warehouse_location_id}",
    response_model=WarehouseLocationResponse
)
def update_warehouse_location(
    warehouse_location_id: int,
    warehouse_location: WarehouseLocationCreate,
    db: Session = Depends(get_db)
):
    return warehouse_location_service.update_location(
        db,
        warehouse_location_id,
        warehouse_location
    )


@router.delete(
    "/warehouse-locations/{warehouse_location_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_warehouse_location(
    warehouse_location_id: int,
    db: Session = Depends(get_db)
):
    warehouse_location_service.delete_location(
        db,
        warehouse_location_id
    )