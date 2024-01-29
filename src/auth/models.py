from pydantic import BaseModel,EmailStr,Field
from uuid import uuid4,UUID
Users = []

class User(BaseModel):
    Id:  UUID = Field(default_factory=uuid4)
    Username: str
    email: EmailStr 
    password: bytes

class RegisterPayload(BaseModel):
    Username: str
    email: EmailStr
    password: str
    confirm_password: str

class LoginPayload(BaseModel):
    email: EmailStr
    password: str