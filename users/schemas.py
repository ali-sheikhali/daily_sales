from pydantic import BaseModel, Field, field_validator


class UserLoginSchema(BaseModel):
    username: str = Field(... ,max_length=150, description="username")
    password: str = Field(... ,max_length=150, description="password")


class UserRegisterSchema(UserLoginSchema):
    password_confirm: str = Field(..., max_length=250, description="confirm password of user")

    @field_validator("password_confirm")
    def check_password_match(cls,password_confirm, validation):
        if not password_confirm == validation.data.get("password"):
            raise ValueError("confirm password not match")
        return password_confirm    