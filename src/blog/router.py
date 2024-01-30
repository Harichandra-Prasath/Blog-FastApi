from fastapi import APIRouter,Response,Depends
from ..auth.dependencies import authorize
from .schemas import Blog,BlogPayload
from pydantic import ValidationError
from ..database import blogCollection
from bson import ObjectId
from .dependencies import Is_owner


Blogrouter = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)


@Blogrouter.post("/create",status_code=201)
async def create(payload:BlogPayload,response:Response,user_id:ObjectId = Depends(authorize)):
    Author_id = user_id       # Current logged in user as the author
    try:
        _blog = Blog(
            Author=Author_id,
            Content=payload.Content,
            Tags=payload.Tags
        )
    except ValidationError:
        response.status_code = 400
        return {"status":"error","Message":"Invalid request body"}
    blog = await blogCollection.insert_one(_blog.model_dump(by_alias=True,exclude=["Id"]))
    return {"status":"Success","Message":"Blog successfully posted","Id":str(blog.inserted_id)}

@Blogrouter.get("/retrieve/{blog_id}",status_code=200,response_model=Blog,response_model_by_alias=False)
async def retrieve(response:Response,blog_id:str): 

    _blog  = await blogCollection.find_one(filter={"_id":ObjectId(blog_id)})
    if _blog:
        return _blog

    response.status_code=404
    return {"Status":"Error","Message":"Resource not found on the server"}

@Blogrouter.put("/update/{blog_id}",status_code=201)
async def edit(payload:BlogPayload,blog_id:str,_:None = Depends(Is_owner)):
    update_dict = {k:v for k,v in payload.model_dump().items()}
    
    _ = await blogCollection.update_one({"_id":ObjectId(blog_id)},{"$set":update_dict})
    return {"Status":"Success","Message":"Blog Succesfully Updated"}

@Blogrouter.delete("/remove/{blog_id}",status_code=204)
async def delete(blog_id:str,_:None=Depends(Is_owner)):
    _ = await blogCollection.delete_one(filter={"_id":ObjectId(blog_id)})

    
