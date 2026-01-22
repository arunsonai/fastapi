"""Cookie Parameter Models¶
If you have a group of cookies that are related, you can create a Pydantic model to declare them.

This would allow you to re-use the model in multiple places and also to declare
validations and metadata for all the parameters at once."""

from fastapi import FastAPI, Cookie
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Cookie Paramater Models"}

"""Cookies with a Pydantic Model¶
Declare the cookie parameters that you need in a Pydantic model, and then declare the parameter as Cookie:"""

class CookieData(BaseModel):
    session_id: int
    fatebook_tracker: str | None = None
    gootle_tracker: str | None = None

@app.get("/items/")
async def get_items(my_item: Annotated[CookieData, Cookie()]):
    return my_item

"""To pass the value and get the output as expected,
    1. Click F12 (developer tools) from the link 'http://127.0.0.1:8000/items/'
    2. Naviate to Application-->Cookies-->Expand Cookies-->Click on the URL. Then add cookies name and values there.
       Example, Name: session_id Value: 6666. After adding values, refresh the page to see the output.

The output of the above code will be as below
{"session_id":6666,"fatebook_tracker":"abc_trk","gootle_tracker":"goo_trk"}"""


"""Forbid Extra Cookies¶
In some special use cases (probably not very common), you might want to restrict the cookies that you want to receive.

Your API now has the power to control its own cookie consent.

You can use Pydantic's model configuration to forbid any extra fields:"""

class ForbidExtra(BaseModel):
    class_id: int
    name: str | None = None
    description: str | None = None
    
    model_config = {"extra" : "forbid"}

@app.get("/forbiddata/")
async def get_data(forbid_extra: Annotated[ForbidExtra, Cookie()]):
    return forbid_extra

"""If a client tries to send some extra cookies, they will receive an error response.

Poor cookie banners with all their effort to get your consent for the API to reject it.

For example, if the client tries to send a associate_detail cookie with a value of
'Soorabadhman', the client will receive an error response telling them that the associate_detail cookie is not allowed:"""