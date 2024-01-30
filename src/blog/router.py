from fastapi import APIRouter,Response,Depends
from ..auth.dependencies import authorize
from .schemas import Blog,BlogPayload,BlogsResponse,DashboardResponse
from pydantic import ValidationError
from ..database import blogCollection,userCollection
from bson import ObjectId
from .dependencies import Is_owner
import datetime
from .utils import paginateDashboard

Blogrouter = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)


@Blogrouter.get("/",status_code=200,response_model=BlogsResponse)
async def get_all(page: int =1,limit: int =10):
    return BlogsResponse(Blogs= await blogCollection.find().skip((page-1)*limit).limit(limit).to_list(limit))


@Blogrouter.post("/create",status_code=201)
async def create(payload:BlogPayload,response:Response,user_id:ObjectId = Depends(authorize)):
    Author_id = user_id       # Current logged in user as the author
    _author = await userCollection.find_one(filter={"_id":Author_id})
    try:
        _blog = Blog(
            Author_Id=str(Author_id),
            Author = _author["Username"],
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
    print(_blog)
    if _blog:
        return _blog
    response.status_code=404
    return {"Status":"Error","Message":"Resource not found on the server"}


@Blogrouter.put("/update/{blog_id}",status_code=201)
async def edit(payload:BlogPayload,blog_id:str,_:None = Depends(Is_owner)):
    update_dict = {k:v for k,v in payload.model_dump().items()}
    update_dict["LastUpdated"] = datetime.datetime.now()
    _ = await blogCollection.update_one({"_id":ObjectId(blog_id)},{"$set":update_dict})
    return {"Status":"Success","Message":"Blog Succesfully Updated"}



@Blogrouter.delete("/remove/{blog_id}",status_code=204)
async def delete(blog_id:str,_:None=Depends(Is_owner)):
    _ = await blogCollection.delete_one(filter={"_id":ObjectId(blog_id)})

    
async def Dashboard(page: int=1,limit: int=10,user_id:ObjectId = Depends(authorize)):

    _user= await userCollection.find_one(filter={"_id":user_id})
    user_tags = _user["Tags"]

    _blogs = [] # Response instance

    # Getting all the blogs with tags of user
    for tag in user_tags:
        cursor =  blogCollection.find(filter={"Tags":{"$in":[tag]}})
        async for doc in cursor:
            _blogs.append(doc)
    
    return DashboardResponse(Blogs=paginateDashboard(page,limit,_blogs))