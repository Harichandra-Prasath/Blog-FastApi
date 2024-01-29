from pydantic import BaseModel,EmailStr,Field
from typing import Optional
from uuid import uuid4,UUID
Users = []


# Avoiding constraints on User Schema as constraints are imposed on payloads
class User(BaseModel):
    Id:  UUID = Field(default_factory=uuid4,frozen=True)
    Username: str = Field(frozen=True)
    FirstName: str
    LastName: str
    Email: EmailStr = Field(frozen=True)
    Password: bytes
    Tags: list

class RegisterPayload(BaseModel):
    Username: str = Field(min_length=3,max_length=30)
    Email: EmailStr = Field(...)
    FirstName: Optional[str]=""
    LastName: Optional[str]=""
    Password: str = Field(min_length=8)
    Confirm_password: str = Field(min_length=8)
    Tags: Optional[list] = []

class LoginPayload(BaseModel):
    Email: EmailStr = Field(...)
    Password: str = Field(...)

class UpdatePayload(BaseModel):
    FirstName:Optional[str]=""
    LastName:Optional[str]=""
    Tags: Optional[list] = []