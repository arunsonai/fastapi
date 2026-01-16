"""Body - Multiple Parameters¶
Now that we have seen how to use Path and Query, let's see more advanced uses of request body declarations.

Mix Path, Query and body parameters¶
First, of course, you can mix Path, Query and request body parameter declarations freely and FastAPI will know what to do.

And you can also declare body parameters as optional, by setting the default to None:"""

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel, Field
from typing import Annotated, Literal

app = FastAPI()
@app.get("/")
async def get_root():
    return {"message": "Hello Body-Multi Parameters"}

class Items(BaseModel):
    item_id: int
    item_name: str | None = None

@app.put("/multiparams/{params_id}")
async def get_params(params_id: Annotated[str, Path(title="Multiple Parameters",
                                                    description="This is a multi parameter model",
                                                    min_length=3,
                                                    max_length=6)],
                     multiparam: Items | None = None,
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
    "item_id": "6",
    "item_name": "Gugan",
}
But you can also declare multiple body parameters, e.g. item and user:
"""
class UserDetails(BaseModel):
    emp_id: int
    name: str | None = None

@app.put("/users/{user_id}")
async def user_details(user_id: int, item: Items, user: UserDetails):
    results = {"User ID" : user_id, "Item Details" : item, "Users" : user}
    return results

"""Singular values in body¶
The same way there is a Query and Path to define extra data for query and path parameters, FastAPI provides an equivalent 'Body'.

For example, extending the previous model, you could decide that you want to have another key
'importance' in the same body, besides the item and user.

If you declare it as is, because it is a singular value, FastAPI will assume that it is a query parameter.

But you can instruct FastAPI to treat it as another body key using 'Body':
Note: The 'body' method"""

@app.put("/albums/{album_id}")
async def get_albums(album_id: int, item_id: Items, user_id: UserDetails, importance: Annotated[str, Body()]):
    results = {"Album Details" : album_id, "Item Details" : item_id, "User Details" : user_id, "Importance" : importance}
    return results

