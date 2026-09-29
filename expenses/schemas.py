from pydantic import BaseModel


class ExpensesGetAllResponseSchemas(BaseModel):
    id: int
    amount: float
    date: str
    store_id: int
    description: str

    class Config:
        orm_mode = True


class ExpensesCreateRequestSchemas(BaseModel):
    store_id: int
    amount: float
    description: str