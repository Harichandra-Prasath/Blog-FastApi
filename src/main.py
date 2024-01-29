from fastapi import FastAPI
from src.auth.router import Authrouter
from src.blog.router import Blogrouter

app = FastAPI()
v1 = FastAPI()

app.mount("/api/v1",v1)
v1.include_router(router=Authrouter)
v1.include_router(router=Blogrouter)
