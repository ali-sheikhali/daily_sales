from pydantic import BaseModel, Field



class StoreManagerCreateSchema(BaseModel):
    owner_id: int = Field(..., description="owner id of store")
    store_id: int = Field(..., description="store that manager")

class StoreManagerListSchema(StoreManagerCreateSchema):
    is_active: bool = Field(..., description="store manager is active or not")
