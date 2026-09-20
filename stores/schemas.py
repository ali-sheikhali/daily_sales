from pydantic import BaseModel, Field


class StoreCreateSchema(BaseModel):
    name : str = Field(..., max_length=150, description="store name")
    owner_id: int = Field(..., description="owner that make store")

class StoreListSchema(StoreCreateSchema):
    pass    


class StoreDetailSchema(BaseModel):
    owner_id: int = Field(..., description="owner that make store")
