from pydantic import BaseModel,Field
from uuid import UUID,uuid4
import datetime 
from typing import Optional


Blogs = []

class Blog(BaseModel):
    Id: UUID = Field(default_factory=uuid4,frozen=True)
    Author: UUID = Field(frozen=True)
    Content: str
    CreatedAt: datetime.datetime = Field(default_factory=datetime.datetime.now,frozen=True)
    LastUpdated: datetime.datetime = Field(default_factory=datetime.datetime.now)
    Tags: list

class BlogPayload(BaseModel):
    Content:str = Field(min_length=10,max_length=500)
    Tags: Optional[list]=[]