from fastapi import APIRouter,Response,Depends
from .schemas import RegisterPayload,User,LoginPayload,UpdatePayload,Users
from .utils import get_password_hash,verify_password,generate_jwt
from .dependencies import authorize
from pydantic import ValidationError
import datetime


Authrouter = APIRouter(
    prefix="/accounts",
    tags = ["Accounts"],
)

@Authrouter.post("/register",status_code=201)
def register(payload: RegisterPayload,response:Response):

    # Bad request , passwords didnt match
    if payload.Password!=payload.Confirm_password:
        response.status_code = 400
        return {"Status":"Error","Message":"Passwords do not match"}
    
    # Create an user
    try:
        user = User(Username=payload.Username,
                    Email=payload.Email,
                    Password=get_password_hash(payload.Password),
                    Tags=payload.Tags,
                    FirstName=payload.FirstName,
                    LastName=payload.LastName)
        
    except ValidationError:
        response.status_code = 400
        return {"Status":"Error","Message":"Invalid request body"}
    
    Users.append(user)
    return {"Status":"Success","Message":"user successfully registered","Id":user.Id}

@Authrouter.post("/login",status_code=200)
def login(response:Response,payload: LoginPayload):

    Email = payload.Email
    for user in Users:
        if user.Email==Email:
            if verify_password(payload.Password,user.Password):

                #Generate jwt with payload containing the username
                _token = generate_jwt(user.Username)

                #setting cookie valid for 30 days
                response.set_cookie(key="jwt",value=_token,max_age=30*24*60*60)
                return {"Status":"Success","Message":"You are logged in."}
            

    response.status_code = 401
    return {"Status":"Error","Message":"Invalid credentials..Try again"}


@Authrouter.put("/update",status_code=201)
def update(payload:UpdatePayload,user: User=Depends(authorize)):
    user.FirstName = payload.FirstName
    user.LastName = payload.LastName
    user.Tags = payload.Tags
    return {"Status":"Success","Message":"Profile Succesfully Updated"}

@Authrouter.get("/logout",status_code=200)
def logout(response:Response,user: User=Depends(authorize)):
    response.set_cookie(key="jwt",value=None,expires=datetime.datetime.now(tz=datetime.timezone.utc)-datetime.timedelta(days=1))
    return {"Status":"Success","Message":"Logged out successfully"}