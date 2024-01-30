from fastapi import APIRouter,Response,Depends
from .schemas import RegisterPayload,User,LoginPayload,UpdatePayload
from .utils import verify_password,generate_jwt
from .dependencies import authorize,RegisterValidator
from pydantic import ValidationError
import datetime
from ..database import userCollection
from bson import ObjectId

Authrouter = APIRouter(
    prefix="/accounts",
    tags = ["Accounts"],
)

@Authrouter.post("/register",status_code=201)
async def register(payload: RegisterPayload,_user:User=Depends(RegisterValidator)):    
    
    # Save the model
    user = await userCollection.insert_one(_user.model_dump(by_alias=True,exclude=["Id"]))
    return {"Status":"Success","Message":"User registered Successfully","Id":str(user.inserted_id)}


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

@Authrouter.get("/profile",status_code=200,response_model=User,response_model_by_alias=False,response_model_exclude="Password")
async def profile(response:Response,user_id:ObjectId = Depends(authorize)):
    user = await userCollection.find_one(filter={"_id":user_id})
    return user