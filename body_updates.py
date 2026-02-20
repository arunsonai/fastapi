from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Body Updates"}

"""Body - Updates¶
Update replacing with PUT¶
To update an item you can use the HTTP PUT operation.

You can use the jsonable_encoder to convert the input data to data that can be stored as JSON (e.g. with a NoSQL database).
For example, converting datetime to str."""

class Items(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] | None = []


things = {
    "Murugan" : {
        "name" : "Murugan",
        "description" : "God Of War",
        "price" : 666666
    },
    "Senthil" : {
        "name" : "Senthil",
        "description" : "Thiruchendilandavar",
        "price" : 6666.66,
        "tax" : 66.6666
    },
    "Shanmugar" : {
        "name" : "Shanmuga",
        "description" : "Killer of Soorabadhman",
        "price" : 666.666,
        "tax" : 6.66666,
        "tags" : ["Shanmugar", "JayanthiNathar", "Thirucheeralaivai Murugan"]
    }
}

@app.get("/details/{id}", response_model=Items)
async def updates(id: str):
    return things[id]

@app.put("/conversions/{id}", response_model=Items)
async def get_conversions(id: str, my_item: Items):
    json_conversion = jsonable_encoder(my_item)
    things[id] = json_conversion
    return things

"""Using Pydantic's exclude_unset parameter¶
If you want to receive partial updates, it's very useful to use the parameter exclude_unset in Pydantic's model's .model_dump().

Like item.model_dump(exclude_unset=True).

That would generate a dict with only the data that was set when creating the item model, excluding default values.

Then you can use this to generate a dict with only the data that was set (sent in the request), omitting default values:"""


@app.put("/items/{item_id}",)
async def get_items(item_id: str, item: Items) -> Items:
    stored_data = things[item_id]
    stored_item_model = Items(**stored_data)
    update_item = item.model_dump(exclude_unset=True)
    merged_data = Items(**stored_item_model.model_dump(), **update_item)
    update_model = Items(**merged_data)
    things[item_id] = jsonable_encoder(update_model)
    return update_model