"""Global Dependencies¶
For some types of applications you might want to add dependencies to the whole application.

Similar to the way you can add dependencies to the path operation decorators, you can add them to the FastAPI application.

In that case, they will be applied to all the path operations in the application:"""


from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Annotated

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

app = FastAPI(dependencies=[Depends(verify_key), Depends(verify_token)])

@app.get("/")
async def get_root():
    return {"message" : "Hello global_dependencies"}