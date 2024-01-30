from ..database import blogCollection
from ..auth.dependencies import authorize
from fastapi import HTTPException,Depends
from bson import ObjectId

async def Is_owner(blog_id: str,user_id:ObjectId = Depends(authorize)):
    _blog = await blogCollection.find_one(filter={"_id":ObjectId(blog_id)})
    if _blog:
        if _blog["Author"]!=user_id:
            raise HTTPException(status_code=403,detail={"Status":"Error",
                                                        "Message":"Forbidden...You dont have permission to perform this action"})
    else:   
        raise HTTPException(status_code=404,detail={"Status":"Failed","Message":"Resource not found on the server"})