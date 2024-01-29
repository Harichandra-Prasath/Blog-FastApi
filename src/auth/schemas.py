from pydantic import BaseModel,EmailStr,Field
from typing import Optional
from uuid import uuid4,UUID
Users = []

class User(BaseModel):
    Id:  UUID = Field(default_factory=uuid4)
    Username: str
    FirstName: str
    LastName: str
    Email: EmailStr 
    Password: bytes
    Tags: list

class RegisterPayload(BaseModel):
    Username: str
    Email: EmailStr
    FirstName: Optional[str]=""
    LastName: Optional[str]=""
    Password: str
    Confirm_password: str
    Tags: Optional[list] = []

class LoginPayload(BaseModel):
    Email: EmailStr
    Password: str

class UpdatePayload(BaseModel):
    FirstName:Optional[str]=""
    LastName:Optional[str]=""
    Tags: Optional[list] = []