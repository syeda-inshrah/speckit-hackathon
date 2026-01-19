from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID


class UserSignup(BaseModel):
    """Schema for user signup request"""
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    name: str = Field(min_length=1, max_length=100)


class UserSignin(BaseModel):
    """Schema for user signin request"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user data in responses"""
    id: UUID
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Schema for authentication response with token"""
    token: str
    user: UserResponse
