from pydantic import BaseModel


class OrderCreate(BaseModel):
    order_number: str
    status: str
    priority: str
    assigned_worker_id: int | None = None


class OrderResponse(BaseModel):
    id: int
    order_number: str
    status: str
    priority: str
    assigned_worker_id: int | None = None