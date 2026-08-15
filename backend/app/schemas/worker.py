from pydantic import BaseModel


class WorkerCreate(BaseModel):
    employee_code: str
    name: str
    status: str
    current_location_id: int | None = None


class WorkerResponse(BaseModel):
    id: int
    employee_code: str
    name: str
    status: str
    current_location_id: int | None = None