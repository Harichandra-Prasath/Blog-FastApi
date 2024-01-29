from fastapi import Request,Response,HTTPException
import jwt
from .schemas import Users

def authorize(request:Request,response:Response):
    token = request.cookies.get("jwt",None)
    if token:
        try:
            payload = jwt.decode(token, key="Secret",algorithms="HS256")
            for user in Users:
                if payload["username"]==user.Username:
                    return user

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401,detail={"Status":"Error",
                                                        "Message":"JWT Expired"})
        except:
            raise HTTPException(status_code=401,detail={"Status":"Error",
                                                        "Message":"Invalid Token"})
    else:
        raise HTTPException(status_code=401,detail={"Status":"Error",
                                                    "Message":"No session or session expired..Login and Try again"})