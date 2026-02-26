from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello global_dependencies"}