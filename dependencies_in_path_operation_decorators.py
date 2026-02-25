from fastapi import FastAPI
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Dependencies in path operation decorators"}
