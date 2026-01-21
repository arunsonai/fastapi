"""Cookie Parameters¶
You can define Cookie parameters the same way you define Query and Path parameters.

Import Cookie¶
First import Cookie:"""

from fastapi import FastAPI, Cookie
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Cookie Parameters"}

@app.get("/cookiedata/")
async def get_data(ads_id: Annotated[str | None, Cookie()] = None):
    return {"Message" : ads_id}