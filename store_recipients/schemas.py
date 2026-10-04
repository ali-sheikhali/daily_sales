from pydantic import BaseModel, Field
from datetime import datetime


class StoreRecipientSchema(BaseModel):
    id: int
    store_id: int
    phone_number: str
    is_active: bool
    create_at: datetime
    update_at: datetime

class StoreRecipientCreateSchema(BaseModel):
    store_id: int
    phone_number: str


class StoreRecipientDetailSchema(StoreRecipientSchema):
    pass

class StoreRecipientUpdateSchema(BaseModel):
    phone_number: str | None = None
    is_active: bool | None = None
    