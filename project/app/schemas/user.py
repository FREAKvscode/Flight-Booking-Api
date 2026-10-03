from pydantic import BaseModel, EmailStr, Field


class SignupSchema(BaseModel):
    fio: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class ProfileUpdateSchema(BaseModel):
    fio: str | None = None
    avatar: str | None = None


