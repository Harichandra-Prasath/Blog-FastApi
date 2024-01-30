from fastapi import APIRouter,Response,Depends
from .schemas import RegisterPayload,User,LoginPayload,UpdatePayload
from .utils import get_password_hash,verify_password,generate_jwt
from .dependencies import authorize
from pydantic import ValidationError
import datetime
from ..database import userCollection
from bson import ObjectId

Authrouter = APIRouter(
    prefix="/accounts",
    tags = ["Accounts"],
)

@Authrouter.post("/register",status_code=201)
async def register(payload: RegisterPayload,response:Response):

    # Bad request , passwords didnt match
    if payload.Password!=payload.Confirm_password:
        response.status_code = 400
        return {"Status":"Error","Message":"Passwords do not match"}
    
    try:
        # User instance
        _user = User(Username=payload.Username,
                    Email=payload.Email,
                    Password=get_password_hash(payload.Password),
                    Tags=payload.Tags,
                    FirstName=payload.FirstName,
                    LastName=payload.LastName)
    
    except ValidationError:
        response.status_code = 400
        return {"Status":"Error","Message":"Invalid request body"}
    
    # Save the model
    user = await userCollection.insert_one(_user.model_dump(by_alias=True,exclude=["Id"]))
    return await userCollection.find_one(filter={"_id":user.inserted_id})

@Authrouter.post("/login",status_code=200)
async def login(response:Response,payload: LoginPayload):

    _Email = payload.Email
    user = await userCollection.find_one(filter={"Email":_Email})
    if user:
            if verify_password(payload.Password,user["Password"]):

                #Generate jwt with payload containing the username
                _token = generate_jwt(user["Username"])

                #setting cookie valid for 30 days
                response.set_cookie(key="jwt",value=_token,max_age=30*24*60*60)
                return {"Status":"Success","Message":"You are logged in."}
            

    response.status_code = 401
    return {"Status":"Error","Message":"Invalid credentials..Try again"}


@Authrouter.put("/update",status_code=201)
async def update(payload:UpdatePayload,user_id:ObjectId = Depends(authorize)):
    
    update_dict = {k:v for k,v in payload.model_dump().items()}
    
    _ = await userCollection.update_one({"_id":user_id},{"$set":update_dict})
    return {"Status":"Success","Message":"Profile Succesfully Updated"}

@Authrouter.get("/logout",status_code=200)
async def logout(response:Response,user_id:ObjectId = Depends(authorize)):
    response.set_cookie(key="jwt",value=None,expires=datetime.datetime.now(tz=datetime.timezone.utc)-datetime.timedelta(days=1))
    return {"Status":"Success","Message":"Logged out successfully"}