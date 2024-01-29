from fastapi import APIRouter,Response,Depends
from ..auth.schemas import User
from ..auth.dependencies import authorize
from .schemas import Blog,BlogPayload,Blogs
from pydantic import ValidationError
from uuid import UUID
import datetime

Blogrouter = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)


@Blogrouter.post("/create",status_code=201)
def create(payload:BlogPayload,response:Response,user:User= Depends(authorize)):
    Author_id = user.Id       # Current logged in user as the author
    try:
        blog = Blog(
            Author=Author_id,
            Content=payload.Content,
            Tags=payload.Tags
        )
    except ValidationError:
        response.status_code = 400
        return {"status":"error","Message":"Invalid request body"}
    Blogs.append(blog)
    return {"status":"Success","Message":"Blog successfully posted","Id":blog.Id}

@Blogrouter.get("/{blog_id}",status_code=200,response_model=Blog)
def retrieve(response:Response,blog_id:UUID): 
    for blog in Blogs:
        if blog.Id==blog_id:
            return blog
    response.status_code=404
    return {"Status":"Error","Message":"Resource not found on the server"}

@Blogrouter.put("/update/{blog_id}",status_code=201)
def edit(payload:BlogPayload,response:Response,blog_id:UUID,user:User=Depends(authorize)):
    for blog in Blogs:
        if blog.Id==blog_id:
            if blog.Author!=user.Id:
                response.status_code=403      # Current logged user is not the author
                return {"Status":"Error","Message":"Forbidden. You dont have permission for this action"}
            blog.Content = payload.Content
            blog.Tags = payload.Tags
            blog.LastUpdated = datetime.datetime.now()
            return {"Status":"Success","Message":"Blog has been updated successfully"}
    
    response.status_code=404
    return {"Status":"Success","Message":"Resource not found on the server"}


@Blogrouter.delete("/remove/{blog_id}",status_code=204)
def delete(response:Response,blog_id:UUID,user:User=Depends(authorize)):
    for blog in Blogs:
        if blog.Id==blog_id:
            if blog.Author!=user.Id:
                response.status_code=403      # Current logged user is not the author
                return {"Status":"Error","Message":"Forbidden. You dont have permission for this action"}
            Blogs.remove(blog)
    
    response.status_code=404
    return {"Status":"Success","Message":"Resource not found on the server"}
