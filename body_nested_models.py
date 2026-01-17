from fastapi import FastAPI
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Body Nested Models"}

"""Body - Nested Models¶
With FastAPI, you can define, validate, document, and use arbitrarily deeply nested models (thanks to Pydantic).

List fields¶
You can define an attribute to be a subtype. For example, a Python list:"""

class Tables(BaseModel):
    design: int | None = None
    size: float
    structure: list = []

@app.put("/chairs/{chair_id}")
async def get_tables(chair_id: int, table: Tables):
    results = {"Chair Details" : chair_id, "Table Details" : table}
    return results

"""This will make 'structure' be a list, although it doesn't declare the type of the elements of the list.

List fields with type parameter¶
But Python has a specific way to declare lists with internal types, or "type parameters":

Declare a list with a type parameter¶
To declare types that have type parameters (internal types), like list, dict, tuple,
pass the internal type(s) as "type parameters" using square brackets: [ and ]


my_list: list[str]
That's all standard Python syntax for type declarations.

Use that same standard syntax for model attributes with internal types.

So, in our example, we can make 'structure' be specifically a "list of strings":"""

class FModifiedTables(BaseModel):
    design: int | None = None
    size: float
    structure: list[str] = []

@app.put("/fmodtables/{chair_id}")
async def fmod_tables(chair_id: int, table: Tables):
    results = {"Chair Details" : chair_id, "Table Details" : table}
    return results

"""Set types¶
But then we think about it, and realize that tags shouldn't repeat, they would probably be unique strings.

And Python has a special data type for sets of unique items, the set.

Then we can declare tags as a set of strings:"""

class SModTables(BaseModel):
    design: int | None = None
    size: float
    structure: set[str] = set()

@app.put("/smodtables/{chair_id}")
async def smod_tables(chair_id: int, table: Tables):
    results = {"Chair Details" : chair_id, "Table Details" : table}
    return results

"""With this, even if you receive a request with duplicate data, it will be converted to a set of unique items.

And whenever you output that data, even if the source had duplicates, it will be output as a set of unique items.

And it will be annotated / documented accordingly too."""


"""Nested Models¶
Each attribute of a Pydantic model has a type.

But that type can itself be another Pydantic model.

So, you can declare deeply nested JSON "objects" with specific attribute names, types and validations.

All that, arbitrarily nested.

Define a submodel¶
For example, we can define an Image model:"""

class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float
    tags: set[str] = set()
    image: Image | None = None

@app.put("items/{item_id}")
async def update_item(item_id: str, item: Item):
    results = {"Item_ID" : item_id, "Item Details" : item}
    return results



    