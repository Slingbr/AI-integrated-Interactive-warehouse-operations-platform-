from pydantic import BaseModel


class PickRequest(BaseModel):

    quantity: int