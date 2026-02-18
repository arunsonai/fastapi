from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello json compatible encoder"}

"""JSON Compatible Encoder¶
There are some cases where you might need to convert a data type (like a Pydantic model) to something compatible with JSON (like a dict, list, etc).

For example, if you need to store it in a database.

For that, FastAPI provides a jsonable_encoder() function.

Using the jsonable_encoder¶
Let's imagine that you have a database fake_db that only receives JSON compatible data.

For example, it doesn't receive datetime objects, as those are not compatible with JSON.

So, a datetime object would have to be converted to a str containing the data in ISO format.

The same way, this database wouldn't receive a Pydantic model (an object with attributes), only a dict.

You can use jsonable_encoder for that.

It receives an object, like a Pydantic model, and returns a JSON compatible version:"""

# Remember to import datetime from datetime
class EncoderItem(BaseModel):
    name: str
    description: str | None = None
    joining_date: datetime

details = {}

# Remember to import jsonable_encoder from fastapi.encoders
@app.put("/users/{id}")
async def get_details(id: str, item: EncoderItem):
    json_compatible_data = jsonable_encoder(item)
    details[id] = json_compatible_data
    return details[id]