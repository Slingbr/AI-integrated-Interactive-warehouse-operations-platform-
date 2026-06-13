from pydantic import BaseModel


class ProductCreate(BaseModel):
    sku: str
    name: str
    quantity: int
    aisle: str
    shelf: str

class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    quantity: int
    aisle: str
    shelf: str

    class Config:
        from_attributes = True