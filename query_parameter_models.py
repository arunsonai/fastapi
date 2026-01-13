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
    offset: int =  Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items/")
async def get_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


