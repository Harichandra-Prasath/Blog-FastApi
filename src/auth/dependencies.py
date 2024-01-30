from fastapi import Request,HTTPException
import jwt
from ..database import userCollection

async def authorize(request:Request):
    token = request.cookies.get("jwt",None)
    if token:
        try:
            payload = jwt.decode(token, key="Secret",algorithms="HS256")
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