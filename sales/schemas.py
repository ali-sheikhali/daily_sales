from pydantic import BaseModel, Field
from datetime import datetime

class SalesCreateSchema(BaseModel):
    amount: float = Field(..., gt= 0,)
    store_id : int

class SalesAllSalesSchema(SalesCreateSchema):
    id: int
    sales_date: datetime