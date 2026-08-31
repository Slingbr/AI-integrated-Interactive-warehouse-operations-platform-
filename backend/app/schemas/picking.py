from pydantic import BaseModel


class PickRequest(BaseModel):
    worker_id: int
    quantity: int