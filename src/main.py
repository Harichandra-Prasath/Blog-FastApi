from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def index():
    return {"Status":"Sucess","Message":"Init success"}