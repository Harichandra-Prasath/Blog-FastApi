from fastapi import FastAPI
from src.auth.router import Authrouter
from src.blog.router import Blogrouter,Dashboard
from src.blog.schemas import DashboardResponse

app = FastAPI()
v1 = FastAPI()

app.mount("/api/v1",v1)

v1.add_api_route("/dashboard",Dashboard,response_model=DashboardResponse) 
v1.include_router(router=Authrouter)      # Auth and User router
v1.include_router(router=Blogrouter)      # Blogs router
