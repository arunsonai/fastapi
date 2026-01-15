from fastapi import FastAPI, Query
from typing import Annotated, Literal
from pydantic import BaseModel, Field

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message": "Hello Query parameter Models"}

"""Query Parameter Models¶
If you have a group of query parameters that are related, you can create a Pydantic model to declare them.

This would allow you to re-use the model in multiple places and also to declare
validations and metadata for all the parameters at once.

Query Parameters with a Pydantic Model¶
Declare the query parameters that you need in a Pydantic model, and then declare the parameter as Query:"""

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "update_at"] = "created_at"
    tags: list[str] = str

@app.get("/items/")
async def get_items(filter_params: Annotated[FilterParams, Query()]):
    return filter_params

"""Forbid Extra Query Parameters¶
In some special use cases (probably not very common), you might want to restrict the query parameters that you want to receive.

You can use Pydantic's model configuration to forbid any extra fields:"""

class ForbidExtra(BaseModel):
    model_config = {"extra" : "forbid"}
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/forbidextra/")
async def forbid_extra(forbid: Annotated[ForbidExtra, Query()]):
    return forbid

"""If a client tries to send some extra data in the query parameters, they will receive an error response.

For example, if the client tries to send a item1 query parameter with a value of Foo, like:

http://127.0.0.1:8000/forbidextra/?limit=11&offset=20&order_by=updated_at&tags=Gemini&tags=OpenAI&item1=Foo

They will receive an error response telling them that the query parameter item1 is not allowed as:

{"detail":[{"type":"extra_forbidden","loc":["query","item1"],"msg":"Extra inputs are not permitted","input":"Foo"}]}"""





