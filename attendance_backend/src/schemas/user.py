from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class UserBase(BaseModel):
    name: str = Field(..., description="Full name of user")
    email: EmailStr = Field(..., description="Email address")
    role: UserRole = Field(..., description="Role of user")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="User password")

class UserUpdate(BaseModel):
    name: str | None = Field(None, description="Full name")
    role: UserRole | None = Field(None, description="Role")

class User(UserBase):
    id: str = Field(..., description="User ID")
    hashed_password: str | None = Field(None, description="Internal: hashed password", exclude=True)

    class Config:
        from_attributes = True
