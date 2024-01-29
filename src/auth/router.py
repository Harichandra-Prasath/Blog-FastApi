from fastapi import APIRouter,Response
from .models import RegisterPayload,User,LoginPayload,Users
from .utils import get_password_hash,verify_password

router = APIRouter(
    prefix="/accounts",
    tags = ["accounts"],
    responses={404:{"description":"Not found"}}
)

@router.post("/register",status_code=201)
def register(payload: RegisterPayload,response:Response):
    if payload.password!=payload.confirm_password:
        response.status_code = 400
        return {"Status":"Error","Message":"Passwords do not match"}
    user = User(Username=payload.Username,
                email=payload.email,
                password=get_password_hash(payload.password))
    Users.append(user)
    return {"Status":"Success","Message":"Success","Id":user.Id}

@router.post("/login",status_code=200)
def login(response:Response,payload: LoginPayload):
    email = payload.email
    for user in Users:
        if user.email==email:
            if verify_password(payload.password,user.password):
                return {"Status":"Success","Message":"You are logged in."}
    response.status_code = 401
    return {"Status":"Error","Message":"Invalid credentials..Try again"}