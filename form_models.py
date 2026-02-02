from fastapi import FastAPI, Form
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Form Models"}

"""Form Models¶
You can use Pydantic models to declare form fields in FastAPI."""

"""Pydantic Models for Forms¶
You just need to declare a Pydantic model with the fields you want to receive as form fields,
and then declare the parameter as Form:"""

class Bicycles(BaseModel):
    name: str
    description: str | None = None

@app.post("/cycles/")
async def get_vehicles(details: Annotated[Bicycles, Form()]):
    return {"message" : details}

"""FastAPI will extract the data for each field from the form data in the request and give you the Pydantic model you defined."""

"""Forbid Extra Form Fields¶
In some special use cases (probably not very common), you might want to restrict the form
fields to only those declared in the Pydantic model. And forbid any extra fields."""

class Televisions(BaseModel):
    chip: str
    cathode_tube: str
    model: str

    model_config = {"forbid" : "extra"}

@app.post("/channels/")
async def get_channel(channel_id: Annotated[Televisions, Form()]):
    return {"message" : channel_id}

"""If a client tries to send some extra data, they will receive an error response.

For example, if the client tries to send the form fields:

chip: MOSFET
cathode_tube: Portal Gun
model: Latest
visual_effect: 4K resolution
They will receive an error response telling them that the field extra is not allowed:


{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "4K resolution"
        }
    ]
}
"""