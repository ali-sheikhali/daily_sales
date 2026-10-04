from pydantic import BaseModel, Field



class StoreManagerCreateSchema(BaseModel):
    store_id: int = Field(..., description="store that manager")

class StoreManagerListSchema(StoreManagerCreateSchema):
    id: int
    is_active: bool = Field(..., description="store manager is active or not")

class StoreManagerUpdate(BaseModel):
    store_id: int
    is_active: bool