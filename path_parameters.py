from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message": "Hello Path Parameters!"}

"""Path Parameters

We can declare path "parameters" or "variables" with the same syntax used by Python format strings:"""

@app.get("/items/{item_id}")
async def get_items(item_id):
    return {"Items are: ": item_id}

"""The value of the path parameter item_id will be passed to your function as the argument item_id.

So, if you run this example and go to http://127.0.0.1:8000/items/foo, you will see a response of:


{"item_id":"foo"}"""


"""Path parameters with types

We can declare the type of a path parameter in the function, using standard Python type annotations:
Remember, we already have a same path operation declared for /items/{item_id} above without type hints (annotations).
So, the first one declared will be the one that FastAPI uses. The code below will not be considered.
Cannot redefine a path operation. and operation matters."""

@app.get("/items/{item_id}")
async def get_items(item_id: int): #In this case, item_id is declared to be an int.
    return {"item id": item_id}

"""Data conversion¶

If you run this example and open your browser at http://127.0.0.1:8000/items/3, you will see a response of:


{"item_id":3}
Notice that the value your function received (and returned) is 3, as a Python int, not a string "3".

So, with that type declaration, FastAPI gives you automatic request "parsing"."""

"""Data validation¶

But if you go to the browser at http://127.0.0.1:8000/items/foo, you will see a nice HTTP error

because the path parameter item_id had a value of "foo", which is not an int.

The same error would appear if you provided a float instead of an int, as in:
http://127.0.0.1:8000/items/4.2

So, with the same Python type declaration, FastAPI gives us data validation.

Notice that the error also clearly states exactly the point where the validation didn't pass.

This is incredibly helpful while developing and debugging code that interacts with our API."""

"""Pydantic¶

All the data validation is performed under the hood by Pydantic, so we get all the benefits from it.
We can use the same type declarations with str, float, bool and many other complex data types."""

"""Order matters¶
When creating path operations, we can find situations where we have a fixed path.

Like /users/me, let's say that it's to get data about the current user.

And then you can also have a path /users/{user_id} to get data about a specific user by some user ID.

Because path operations are evaluated in order, we need to make sure that the path for /users/me is 
declared before the one for /users/{user_id}:"""

@app.get("/users/me")
async def get_me():
    return {"user id": "This is current item"}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"User Id": user_id}

"""Otherwise, the path for /users/{user_id} would match also for /users/me, "thinking" that 
it's receiving a parameter user_id with a value of "me"."""

"""Cannot redefine a path operation

Similarly, we cannot redefine a path operation:"""

@app.get("/users")
async def get_user():
    return {"Ricky, Martin"}

@app.get("/users")
async def get_user2():
    return {"Jony, Soni"}

"""The first one (get_user() path operation function of path opeartion decorator-users) will
always be used since the path matches first."""

"""Predefined values¶
If you have a path operation that receives a path parameter, but you want the possible valid 
path parameter values to be predefined, you can use a standard Python Enum.

Create an Enum class¶
Import Enum and create a sub-class that inherits from str and from Enum.

By inheriting from str the API docs will be able to know that the values must be 
of type string and will be able to render correctly.

Then create class attributes with fixed values, which will be the available valid values:"""

from enum import Enum
class ModelName(str, Enum):
    alexnet = "AlexNet"
    resnet = "ResNet"
    lenet = "LeNet"

# Declare a path parameter¶
# Then create a path parameter with a type annotation using the enum class we created (ModelName):
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet: # We can compare it with the enumeration member in our created enum ModelName:
        return {"Model Name": model_name, "message": "Best CV model"} # The value of the path parameter will be an enumeration member.
    if model_name.value == "LeNet":
        return {"Model Name": model_name, "message": "Developed by Yann LeCun"}
    return ModelName.resnet.value, {"message": "Residual Network"}
"""We can get the actual value (a str in this case) using model_name.value, or in general, our_enum_member.value:"""

"""Get the enumeration value¶
Return enumeration members¶
You can return enum members from your path operation, even nested in a JSON body (e.g. a dict).

They will be converted to their corresponding values (strings in this case) before returning them to the client:"""

"""Path parameters containing paths¶
Let's say you have a path operation with a path /files/{file_path}.

But you need file_path itself to contain a path, like home/johndoe/myfile.txt.

So, the URL for that file would be something like: /files/home/johndoe/myfile.txt."""

"""OpenAPI support¶
OpenAPI doesn't support a way to declare a path parameter to contain a path inside, as that could lead to
scenarios that are difficult to test and define.

Nevertheless, you can still do it in FastAPI, using one of the internal tools from Starlette.

And the docs would still work, although not adding any documentation telling that the parameter should contain a path."""


"""Path convertor¶
Using an option directly from Starlette you can declare a path parameter containing a path using a URL like:


/files/{file_path:path}
In this case, the name of the parameter is file_path, and the last part, :path, tells it that the parameter should match any path.

So, we can use it with:"""

@app.get("/files/{file_path:path}")
async def get_path(file_path: str):
    return {"File Path": file_path}
