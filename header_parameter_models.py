"""Header Parameter Models¶
If you have a group of related header parameters, you can create a Pydantic model to declare them.

This would allow you to re-use the model in multiple places and also to declare
validations and metadata for all the parameters at once."""

from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_rot():
    return {"message" : "Hello Header Parameter Models"}

class CustomHeader(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/createheaders/")
async def create_headers(headerparam: Annotated[CustomHeader, Header()]):
    return headerparam

"""Forbid Extra Headers¶
In some special use cases (probably not very common), you might want to restrict the headers that you want to receive.

You can use Pydantic's model configuration to forbid any extra fields:"""

class ForbidExtra(BaseModel):
    host: str
    save_data: bool | None = None
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = [] 

    model_config = {"forbid" : "extra"}

@app.get("/forbid/")
async def remove_data(dataremoval: Annotated[ForbidExtra, Header()]):
    return dataremoval

"""If a client tries to send some extra headers, they will receive an error response.

For example, if the client tries to send a tool header with a value of 'Soorabadhman',
they will receive an error response telling them that the header parameter tool is not allowed:


{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "Soorabadhman",
        }
    ]
}
"""

"""Disable Convert Underscores¶
The same way as with regular header parameters, when you have underscore characters in
the parameter names, they are automatically converted to hyphens.

For example, if you have a header parameter save_data in the code, the expected
HTTP header will be save-data, and it will show up like that in the docs.

If for some reason you need to disable this automatic conversion, you can do it as well
for Pydantic models for header parameters."""

class ConvertUnderscore(BaseModel):
    host: str
    save_data: bool | None = None
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = [] 

@app.get("/Underscore/")
async def convert_underscore(underscore_param: Annotated[ConvertUnderscore, Header(convert_underscores=True)]):
    return underscore_param