from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.warehouse_location import WarehouseLocation
from app.schemas.warehouse_location import WarehouseLocationCreate


def create_location(
    db: Session,
    warehouse_location: WarehouseLocationCreate
) -> WarehouseLocation:

    new_location = WarehouseLocation(
        code=warehouse_location.code,
        name=warehouse_location.name,
        location_type=warehouse_location.location_type,
        x_coordinate=warehouse_location.x_coordinate,
        y_coordinate=warehouse_location.y_coordinate
    )

    db.add(new_location)
    db.commit()
    db.refresh(new_location)

    return new_location


def update_location(
    db: Session,
    warehouse_location_id: int,
    warehouse_location: WarehouseLocationCreate
) -> WarehouseLocation:

    existing_location = (
        db.query(WarehouseLocation)
        .filter(WarehouseLocation.id == warehouse_location_id)
        .first()
    )

    if existing_location is None:
        raise HTTPException(
            status_code=404,
            detail="Warehouse location not found"
        )

    for key, value in warehouse_location.model_dump().items():
        setattr(existing_location, key, value)

    db.commit()
    db.refresh(existing_location)

    return existing_location


def delete_location(
    db: Session,
    warehouse_location_id: int
):

    existing_location = (
        db.query(WarehouseLocation)
        .filter(WarehouseLocation.id == warehouse_location_id)
        .first()
    )

    if existing_location is None:
        raise HTTPException(
            status_code=404,
            detail="Warehouse location not found"
        )

    db.delete(existing_location)
    db.commit()


def get_locations(
    db: Session
) -> list[WarehouseLocation]:

    return db.query(WarehouseLocation).all()


def get_location(
    db: Session,
    warehouse_location_id: int
) -> WarehouseLocation:

    location = (
        db.query(WarehouseLocation)
        .filter(WarehouseLocation.id == warehouse_location_id)
        .first()
    )

    if location is None:
        raise HTTPException(
            status_code=404,
            detail="Warehouse location not found"
        )

    return location