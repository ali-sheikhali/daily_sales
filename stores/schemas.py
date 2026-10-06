from pydantic import BaseModel, Field


class StoreCreateSchema(BaseModel):
    name : str = Field(..., max_length=150, description="store name")

class StoreListSchema(StoreCreateSchema):
    id: int
    owner_id: int = Field(..., description="owner that make store") 
    pass    


class StoreDetailSchema(BaseModel):
    id: int
    name: str
    owner_id: int = Field(..., description="owner that make store")
