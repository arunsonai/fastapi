"""Body - Multiple Parameters¶
Now that we have seen how to use Path and Query, let's see more advanced uses of request body declarations.

Mix Path, Query and body parameters¶
First, of course, you can mix Path, Query and request body parameter declarations freely and FastAPI will know what to do.

And you can also declare body parameters as optional, by setting the default to None:"""

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Annotated, Literal

app = FastAPI()
@app.get("/")
async def get_root():
    return {"message": "Hello Body-Multi Parameters"}

class MultipleParameters(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, le=100)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.put("/multiparams/{params_id}")
async def get_params(params_id: Annotated[str, Path(title="Multiple Parameters",
                                                    description="This is a multi parameter model",
                                                    min_length=3,
                                                    max_length=6)],
                     multiparam: MultipleParameters | None = None,
                     q: str | None = None):
    final_items = {"Params ID" : params_id}
    if q:
        final_items.update({"Query Parameters" : q})
    if multiparam:
        final_items.update({"Request Body": multiparam})
    return final_items

"""Multiple body parameters¶
In the previous example, the path operations would expect a JSON body with the attributes of an Item, like:

{
    "limit": "25",
    "offset": "25",
    "order_by": "updated_at",
    "tags": ["Arun", "Murugan"]
}
But you can also declare multiple body parameters, e.g. multiparam and user:
"""
class UserDetails(BaseModel):
    emp_id: int
    name: str | None = None

@app.put("/users/{user_id}")
async def user_details(user_id: UserDetails):
    results = {"User ID" : user_id, "Multiple Params" : MultipleParameters, "Users" : UserDetails}
    return results