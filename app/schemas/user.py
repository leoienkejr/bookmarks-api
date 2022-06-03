from pydantic import BaseModel, EmailStr, validator
from ..validators import password_validator


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

    _validate_password = validator('password', allow_reuse=True)(
        password_validator.validate)


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
