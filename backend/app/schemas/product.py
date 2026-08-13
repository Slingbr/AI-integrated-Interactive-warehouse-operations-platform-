from pydantic import BaseModel


class ProductCreate(BaseModel):
    sku: str
    name: str
    quantity: int
    location_id: int

class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    quantity: int
    location_id: int

    class Config:
        from_attributes = True