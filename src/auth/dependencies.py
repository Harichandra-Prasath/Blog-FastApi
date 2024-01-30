from fastapi import Request,HTTPException
import jwt
from ..database import userCollection
from .schemas import RegisterPayload,User
from .utils import get_password_hash
from pydantic import ValidationError
import os

async def authorize(request:Request):
    token = request.cookies.get("jwt",None)
    if token:
        try:
            payload = jwt.decode(token, key=os.getenv("SECRET"),algorithms="HS256")
            user = await userCollection.find_one(filter={"Username":payload["username"]})
            if user:
                return user["_id"]
            else:
                raise HTTPException(status_code=404,detail={"Status":"Error",
                                                            "Message":"User not found"})

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401,detail={"Status":"Error",
                                                        "Message":"JWT Expired"})
        except:
            raise HTTPException(status_code=401,detail={"Status":"Error",
                                                        "Message":"Invalid JWT Token...Login Required to perform this operation"})
    else:
        raise HTTPException(status_code=401,detail={"Status":"Error",
                                                    "Message":"No session or session expired..Login Required to perform this operation"})
    

async def RegisterValidator(payload:RegisterPayload):
    try:
        # User instance
        if payload.Password!=payload.Confirm_password:
            raise HTTPException(status_code=400,detail={"Status":"Error",
                                                    "Message":"Passwords do not match"})
        
        if (await userCollection.find_one(filter={"Username":payload.Username})):
            raise HTTPException(status_code=400,detail={"Status":"Error",
                                                    "Message":"Username already exists"})
        
        if (await userCollection.find_one(filter={"Email":payload.Email})):
            raise HTTPException(status_code=400,detail={"Status":"Error",
                                                    "Message":"Email already exists"})
        
        _user = User(Username=payload.Username,
                    Email=payload.Email,
                    Password=get_password_hash(payload.Password),
                    Tags=payload.Tags,
                    FirstName=payload.FirstName,
                    LastName=payload.LastName)


        return _user
    except ValidationError:
        raise HTTPException(status_code=400,detail={"Status":"Error",
                                                    "Message":"Bad request body"})