from pydantic import BaseModel

class WarehouseLocationCreate(BaseModel):
    code : str
    name : str
    location_type : str
    x_coordinate : int
    y_coordinate : int

class WarehouseLocationResponse(BaseModel):
    id   : int
    code : str
    name : str
    location_type : str
    x_coordinate : int
    y_coordinate : int

    class Config:
        from_attributes = True