from pydantic import BaseModel
from datetime import datetime


class ExpensesGetAllResponseSchemas(BaseModel):
    id: int
    amount: float
    store_id: int
    description: str
    expenses_date: datetime

class ExpensesCreateRequestSchemas(BaseModel):
    store_id: int
    amount: float
    description: str


class ExpensesEditRequestSchemas(BaseModel):
    amount: float | None = None
    description: str | None = None
    expenses_date: datetime | None = None