from typing import Optional
from datetime import datetime
from pydantic import Field
from backend.schemas.common import BaseSchema, AuditSchema

class UserBase(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=3, max_length=100)
    phone: Optional[str] = None
    role: str = "VIEWER"
    status: str = "ACTIVE"

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseSchema):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase, AuditSchema):
    last_login: Optional[datetime] = None
