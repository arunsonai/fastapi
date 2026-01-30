"""Response Model - Return Type¶
You can declare the type used for the response by annotating the path operation function return type.

You can use type annotations the same way you would for input data in function parameters,
you can use Pydantic models, lists, dictionaries, scalar values like integers, booleans, etc."""


from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, EmailStr
from typing import Annotated, Any

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Response Model Return Types"}


class ResponseModel(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

@app.post("/ResponseType/")
async def get_response(response: ResponseModel) -> ResponseModel:
    return response

@app.post("/Electricity/")
async def get_current(param_current: ResponseModel) -> list[ResponseModel]:
    return [
        ResponseModel(
            name="Senthilandavar",
            description="Murugan Name",
            price=666666,
            tax=666.666,
            tags=["ArunagiriNathar", "Gugan", "Dhandayudhani"])
    ]


"""response_model Parameter¶
There are some cases where you need or want to return some data that is not exactly what the type declares.

For example, you could want to return a dictionary or a database object, but declare it as a Pydantic model.
This way the Pydantic model would do all the data documentation, validation, etc. for the object that you
returned (e.g. a dictionary or database object).

If you added the return type annotation, tools and editors would complain with a (correct) error telling
you that your function is returning a type (e.g. a dict) that is different from what you declared (e.g. a Pydantic model).

In those cases, you can use the path operation decorator parameter response_model instead of the return type.

You can use the response_model parameter in any of the path operations:

@app.get()
@app.post()
@app.put()
@app.delete()
etc."""

# Need to import 'Any' subclass from typing module
@app.post("/Sockets/", response_model = ResponseModel)
async def get_sockets(items: ResponseModel) -> Any:
    return items

@app.post("/Floors/", response_model=list[ResponseModel])
async def get_floors(param_floor: ResponseModel) -> Any:
    return [
        ResponseModel(
            name="Valliammai",
            description="Murugan Wife Name",
            price=66.6666,
            tax=6.66,
            tags=["Deivanai", "IndranMagal", "Iravadham"]
        )
    ]

"""Return the same input data¶
Here we are declaring a UserIn model, it will contain a plaintext password:"""

# Remember to import 'EmailStr' class from Pydantic
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    fullname: str | None = None

@app.post("/Emails/")
async def get_password(users: UserIn) -> UserIn:
    return users

"""Add an output model¶
We can instead create an input model with the plaintext password and an output model without it:"""

class InputModel(BaseModel):
    username: str
    password: str
    email: EmailStr
    fullname: str | None = None

class OutputModel(BaseModel):
    username: str
    email: EmailStr
    fullname: str | None = None

@app.post("/DifferentModels/", response_model=OutputModel)
async def get_output(input_model: InputModel) -> Any:
    return input_model

"""Above code, even though our path operation function is returning the same input 'input_model' that contains the password,
we declared the response_model to be our model 'OutputModel', that doesn't include the password.
So, FastAPI will take care of filtering out all the data that is not declared in the output model (using Pydantic).

response_model or Return Type¶

In this case, because the two models are different, if we annotated the function return type as 'OutputModel',
the editor and tools would complain that we are returning an invalid type, as those are different classes.

That's why in this example we have to declare it in the response_model parameter"""


"""Return Type and Data Filtering¶
Now, We wanted to annotate the function with one type,
but we wanted to be able to return from the function something that actually includes more data.

We want FastAPI to keep filtering the data using the response model. So that even though the
function returns more data, the response will only include the fields declared in the response model.

In the previous example, because the classes were different, we had to use the response_model parameter.
But that also means that we don't get the support from the editor and tools checking the function return type.

But in most of the cases where we need to do something like this, we want the model just to filter/remove
some of the data as in this example.

And in those cases, we can use classes and inheritance to take advantage of function type annotations
to get better support in the editor and tools, and still get the FastAPI data filtering.
"""

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(UserIn):
    username: str
    email: EmailStr
    full_name: str | None = None

@app.post("/users/")
async def get_details(user_details: UserOut) -> UserIn:
    return user_details


"""Other Return Type Annotations¶
There might be cases where you return something that is not a valid Pydantic field and you annotate
it in the function, only to get the support provided by tooling (the editor, mypy, etc).

Return a Response Directly¶
The most common case would be returning a Response directly"""

# Remember to import 'Response' from fastapi and 'JSONResponse', 'RedirectResponse' from fastapi.responses
@app.get("/laptops/")
async def get_responses(model_detail: bool = True) -> Response:
    if model_detail:
        return RedirectResponse(url="https://fastapi.tiangolo.com/tutorial/response-model/#return-a-response-directly")
    else:
        return JSONResponse(content={"message" : "This is just a JSON message"})
    

"""Annotate a Response Subclass¶
You can also use a subclass of Response in the type annotation:"""

@app.get("/Nature/")
async def get_nature() -> RedirectResponse:
    return RedirectResponse(url="https://fastapi.tiangolo.com/tutorial/response-model/#return-a-response-directly")

"""This will also work because RedirectResponse is a subclass of Response, and FastAPI will
automatically handle this simple case."""


"""Invalid Return Type Annotations¶
But when you return some other arbitrary object that is not a valid Pydantic type (e.g. a database object)
and you annotate it like that in the function, FastAPI will try to create a Pydantic response model from that
type annotation, and will fail.

The same would happen if you had something like a union between different types where one or more of them
are not valid Pydantic types, for example this would fail"""


"""
@app.get("/portal/")
async def get_portal(webindex: bool = True) -> Response | dict:
    if webindex:
        return RedirectResponse(url="https://fastapi.tiangolo.com/tutorial/response-model/#return-a-response-directly")
    return JSONResponse({"message" : "This is an interdimensional portal"})"""

"""The above code fails because the type annotation is not a Pydantic type and is not just a
single Response class or subclass, it's a union (any of the two) between a Response and a dict."""


"""Disable Response Model¶
Continuing from the example above, you might not want to have the default data validation,
documentation, filtering, etc. that is performed by FastAPI.

But you might want to still keep the return type annotation in the function to get the
support from tools like editors and type checkers (e.g. mypy).

In this case, you can disable the response model generation by setting response_model=None:"""

@app.get("/matches/", response_model=None)
async def get_portal(webindex: bool = True) -> Response | dict:
    if webindex:
        return RedirectResponse(url="https://fastapi.tiangolo.com/tutorial/response-model/#return-a-response-directly")
    return JSONResponse({"message" : "This is an interdimensional portal"})

"""This will make FastAPI skip the response model generation and that way you can have any
return type annotations you need without it affecting your FastAPI application."""