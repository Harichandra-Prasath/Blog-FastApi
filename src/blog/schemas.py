from pydantic import BaseModel,Field,ConfigDict
import datetime 
from typing import Optional
from bson import ObjectId


class Blog(BaseModel):
    Id: Optional[ObjectId] = Field(alias="_id",default=None)
    Author: str
    Author_Id: ObjectId 
    Content: str
    CreatedAt: datetime.datetime = Field(default_factory=datetime.datetime.now)
    LastUpdated: datetime.datetime = Field(default_factory=datetime.datetime.now)
    Tags: list[str]
    model_config = ConfigDict(arbitrary_types_allowed=True,json_encoders={ObjectId: str})

class BlogPayload(BaseModel):
    Content:str = Field(min_length=10,max_length=500)
    Tags: Optional[list]=[]

class BlogsResponse(BaseModel):
    Blogs : list[Blog]

class DashboardResponse(BaseModel):
    Blogs: list[Blog]