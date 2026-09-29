from pydantic import BaseModel
from datetime import datetime


class ExpensesGetAllResponseSchemas(BaseModel):
    id: int
    amount: float
    expenses_date: str
    store_id: int
    description: str
    expenses_date: datetime

class ExpensesCreateRequestSchemas(BaseModel):
    store_id: int
    amount: float
    description: str