from pydantic import BaseModel, Field, field_validator
from typing import Literal

class UserLoginSchema(BaseModel):
    username: str = Field(... ,max_length=150, description="username")
    password: str = Field(... ,max_length=150, description="password")

class UserRegisterSchema(UserLoginSchema):
    password_confirm: str = Field(..., max_length=250, description="confirm password of user")
    role: Literal["owner", "manager"] = Field(..., description="role of user")

    @field_validator("password_confirm")
    def check_password_match(cls, password_confirm, validation):
        if not password_confirm == validation.data.get("password"):
            raise ValueError("confirm password not match")
        return password_confirm    


class UserRegisterResponseSchema(BaseModel):
    id: int = Field(..., description="id of user")
    username: str = Field(..., max_length=150, description="username of user")
    role: Literal["owner", "manager"] = Field(..., description="role of user")


class UserLoginResponseSchema(BaseModel):
    access_token: str = Field(..., description="access token of user")
    token_type: str = Field(..., description="token type of user")
    username: str = Field(..., description="username of user")
    role: Literal["owner", "manager"] = Field(..., description="role of user")
    id: int = Field(..., description="id of user")
    store_id: int | None = Field(default=None, description="store id")