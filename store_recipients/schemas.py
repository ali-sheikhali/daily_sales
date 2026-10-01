from pydantic import BaseModel


class StoreRecipientSchema(BaseModel):
    id: int
    store_id: int
    phone_number: str
    is_active: bool
    created_at: str
    updated_at: str
