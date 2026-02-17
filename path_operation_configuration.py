"""Path Operation Configuration¶
There are several parameters that you can pass to your path operation decorator to configure it.

Warning:
Notice that these parameters are passed directly to the path operation decorator, not to your path operation function."""


"""Response Status Code¶
You can define the (HTTP) status_code to be used in the response of your path operation.

You can pass directly the int code, like 404.

But if you don't remember what each number code is for, you can use the shortcut constants in status:"""


from fastapi import FastAPI, status
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Path Operation Configuration"}

class ItemDetails(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def get_items(item: ItemDetails) -> ItemDetails:
    return item


"""Tags¶
You can add tags to your path operation, pass the parameter tags with a list of str (commonly just one str):"""

@app.post("/tagitems/", tags=["items"])
async def get_tags(tag_items: ItemDetails) -> ItemDetails:
    return tag_items

@app.get("/readitems/", tags=["curtains"])
async def read_items():
    return [{"chairs" : "Foo", "details" : "Name of a person"}]

@app.get("/users/", tags=["Users"])
async def get_users():
    return {"username" : "Senthil Andavar", "details" : "God of war"}


"""Tags with Enums¶
If you have a big application, you might end up accumulating several tags, and you would want to make sure you always use the same tag for related path operations.

In these cases, it could make sense to store the tags in an Enum.

FastAPI supports that the same way as with plain strings:"""


# Remember to import Enum from enum
class Tags(Enum):
    stores = "shops"
    buildings = "construction"
    army = "guns"

@app.get("/store/", tags=[Tags.stores])
async def get_shops():
    return {"cosmetics" : "clenser", "stationary" : "pencils", "automobiles" : "engine cover"}

@app.get("/building/", tags=[Tags.buildings])
async def get_buildings():
    return {"construction" : "Contemporary", "architecture" : "conventional"}

@app.get("/armies/", tags=[Tags.army])
async def get_forces():
    return {"gun" : "AK47", "grenade" : "US M67"}


"""Summary and description¶
You can add a summary and description:"""

@app.post("/customers/",
         summary="This is a summary portion",
         description="The details are described here")
async def get_customers():
    return {"network" : "airtel", "paints" : "asian"}


"""Description from docstring¶
As descriptions tend to be long and cover multiple lines, you can declare the path operation
description in the function docstring and FastAPI will read it from there.

You can write Markdown in the docstring, it will be interpreted and displayed correctly (taking into account docstring indentation)."""

@app.post("/teachers/", summary="Details about Teachers")
async def get_information(info: ItemDetails):
    """ Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item"""
    return info


"""Response description¶
You can specify the response description with the parameter response_description:"""

@app.post("/responses/",
          summary="Response Description",
          response_description="This is the description for response model")
async def get_response(response_detail: ItemDetails) -> ItemDetails:
    """ Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item"""
    return response_detail


"""Deprecate a path operation¶
If you need to mark a path operation as deprecated, but without removing it, pass the parameter deprecated:"""

@app.get("/plants/", tags=["potatoes"])
async def get_plant():
    return [{"Item1" : "Potato", "Item2" : "Onion"}]

@app.get("/animals/", tags=["animal"])
async def get_animal():
    return [{"Item1" : "Tiger", "Item2" : "Lion", "Item3" : "Hippo"}]

@app.get("/veggies/", tags=["potatoes"], deprecated=True)
async def get_veggies():
    return [{"Leaf1" : "curry", "Leaf2" : "coriander", "Leaf3" : "spinach"}]