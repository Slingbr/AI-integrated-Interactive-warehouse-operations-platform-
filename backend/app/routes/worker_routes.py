from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.worker import WorkerCreate, WorkerResponse
from app.services import worker_service

router = APIRouter()


@router.post("/workers", response_model=WorkerResponse)
def create_worker(
    worker: WorkerCreate,
    db: Session = Depends(get_db)
):
    return worker_service.create_worker(db, worker)


@router.get("/workers", response_model=list[WorkerResponse])
def get_workers(
    db: Session = Depends(get_db)
):
    return worker_service.get_workers(db)


@router.get(
    "/workers/{employee_code}",
    response_model=WorkerResponse
)
def get_worker(
    employee_code: str,
    db: Session = Depends(get_db)
):
    return worker_service.get_worker(
        db,
        employee_code
    )


@router.put(
    "/workers/{worker_id}",
    response_model=WorkerResponse
)
def update_worker(
    worker_id: int,
    worker: WorkerCreate,
    db: Session = Depends(get_db)
):
    return worker_service.update_worker(
        db,
        worker_id,
        worker
    )


@router.delete(
    "/workers/{worker_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_worker(
    worker_id: int,
    db: Session = Depends(get_db)
):
    worker_service.delete_worker(
        db,
        worker_id
    )