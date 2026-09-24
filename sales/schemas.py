from pydantic import BaseModel, Field


class SalesCreateSchema(BaseModel):
    amount: float = Field(..., gt= 0,)
    store_id : int

