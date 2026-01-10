"""Request Body¶
When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.

A request body is data sent by the client to your API. A response body is the data your API sends to the client.

Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time, sometimes they only request a path, maybe with some query parameters, but don't send a body.

To declare a request body, you use Pydantic models with all their power and benefits.

Import Pydantic's BaseModel¶
First, you need to import BaseModel from pydantic:"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

"""Create your data model¶
Then you declare your data model as a class that inherits from BaseModel.

Use standard Python types for all the attributes:"""

class Item(BaseModel):
    id: int
    name: str
    description: str | None = None

@app.get("/")
async def get_root():
    return {"message": "Hello Request Body!"}

@app.post("/items/")
async def get_items(item: Item):
    return item

"""The same as when declaring query parameters, when a model attribute has a default value, it is not required. Otherwise, it is required. Use None to make it just optional.

For example, this model above declares a JSON "object" (or Python dict) like:

{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}

...as description and tax are optional (with a default value of None), this JSON "object" would also be valid:

{
    "name": "Foo",
    "price": 45.2
}


Declare it as a parameter¶
To add it to your path operation, declare it the same way you declared path and query parameters:

//async def create_item(item: Item)://
    
...and declare its type as the model you created, Item."""

"""Use the model¶
Inside of the function, you can access all the attributes of the model object directly:"""

class Returns(BaseModel):
    name: str
    tax: float | None = None
    price: float

benefits_store: dict[int, float] = {}

@app.post("/benefits/")
async def file_tax(pay: Returns, benefit_id: int):
    total_price = pay.model_dump()
    if pay.tax is not None:
        total_price = pay.tax + pay.price
    benefits_store[benefit_id] = total_price
    return {"Total Price" : total_price}

"""Request body + path parameters¶
You can declare path parameters and request body at the same time.

FastAPI will recognize that the function parameters that match path parameters should be taken from the
path, and that function parameters that are declared to be Pydantic models should be taken from the request body."""

@app.put("/benefits/{benefit_id}")
async def update_tax(benefit_id: int, pay: Returns):
    return {"Benefit ID": benefit_id, **pay.model_dump()}

@app.get("/benefits/{benefit_id}")
async def get_tax(benefit_id: int):
    return {"Benefit ID": benefit_id, "Total Price" : benefits_store[benefit_id]}

"""Request body + path + query parameters¶
You can also declare body, path and query parameters, all at the same time.

FastAPI will recognize each of them and take the data from the correct place."""

@app.get("/shops/{shop_id}")
async def get_shop(shop_id: int, ret: Returns, qry: str | None = None):
    response = {"Shop ID": shop_id, **ret.model_dump()}
    if qry:
        response.update({"Query": qry})
    return response