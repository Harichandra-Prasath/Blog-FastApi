from fastapi import FastAPI
from src.auth.router import router

app = FastAPI()
app.include_router(router)

