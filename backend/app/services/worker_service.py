from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.worker import Worker
from app.schemas.worker import WorkerCreate


def create_worker(
    db: Session,
    worker: WorkerCreate
) -> Worker:

    new_worker = Worker(
        employee_code=worker.employee_code,
        name=worker.name,
        status=worker.status,
        current_location_id=worker.current_location_id
    )

    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)

    return new_worker

def update_worker(
    db: Session,
    worker_id: int,
    worker: WorkerCreate
) -> Worker:

    existing_worker = (
        db.query(Worker)
        .filter(Worker.id == worker_id)
        .first()
    )

    if existing_worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker not found"
        )

    for key, value in worker.model_dump().items():
        setattr(existing_worker,key,value)

    db.commit()
    db.refresh(existing_worker)

    return existing_worker

def delete_worker(
    db: Session,
    worker_id: int
) -> None:

    existing_worker = (
        db.query(Worker)
        .filter(Worker.id == worker_id)
        .first()
    )

    if existing_worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker not found"
        )

    # delete existing_worker here
    db.delete(existing_worker)
    db.commit()

def get_workers(
    db: Session
) -> list[Worker]:

    return db.query(Worker).all()


def get_worker(
    db: Session,
    worker_employee_code: str
) -> Worker:

    worker = (
        db.query(Worker)
        .filter(Worker.employee_code == worker_employee_code)
        .first()
    )

    if worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker not found"
        )

    return worker