from pydantic import BaseModel,EmailStr,Field,ConfigDict
from typing import Optional
from bson import ObjectId


# Avoiding constraints on User Schema as constraints are imposed on payloads
class User(BaseModel):
    Id: Optional[ObjectId] = Field(alias="_id",default=None)
    Username: str 
    FirstName: str
    LastName: str
    Email: EmailStr 
    Password: str
    Tags: list
    model_config = ConfigDict(arbitrary_types_allowed=True,json_encoders={ObjectId: str})


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