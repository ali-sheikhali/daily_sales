from pydantic import BaseModel, Field


class StoreRecipientSchema(BaseModel):
    id: int
    store_id: int
    phone_number: str
    is_active: bool
    created_at: str
    updated_at: str

class StoreRecipientCreateSchema(BaseModel):
    store_id: int
    phone_number: str
    