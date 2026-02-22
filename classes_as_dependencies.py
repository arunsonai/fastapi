from fastapi import FastAPI, Depends
from typing import Annotated, Any

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Classes as Dependencies!"}


"""What makes a dependency¶
Up to now you have seen dependencies declared as functions.

But that's not the only way to declare dependencies (although it would probably be the more common).

The key factor is that a dependency should be a "callable".

A "callable" in Python is anything that Python can "call" like a function.

So, if you have an object something (that might not be a function) and you can "call" it (execute it) like:


"something()"

or

"something(some_argument, some_keyword_argument="foo")"

then it is a "callable"."""


"""Classes as dependencies¶
You might notice that to create an instance of a Python class, you use that same syntax.

For example:"""

class God():
    def __init__(self, name: str):
        self.name = name

almighty = God(name="Shanmugar")


"""In this case, almighty is an instance of the class God.

And to create almighty, you are "calling" God.

So, a Python class is also a callable.

Then, in FastAPI, you could use a Python class as a dependency.

What FastAPI actually checks is that it is a "callable" (function, class or anything else) and the parameters defined.

If you pass a "callable" as a dependency in FastAPI, it will analyze the parameters for that "callable", and
process them in the same way as the parameters for a path operation function. Including sub-dependencies.

That also applies to callables with no parameters at all. The same as it would be for path operation functions with no parameters.

Then, we can change the dependency "dependable" common_parameters from above to the class CommonQueryParams:
"""

fake_item_db = [{"item_name" : "Foo"}, {"item_name" : "Bar"}, {"item_name" : "Baz"}]

class CommonQeuryParams():
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: Annotated[CommonQeuryParams, Depends(CommonQeuryParams)]):
    response = {}
    if commons.q:
        response.update({"q" : commons.q})
    db_items = fake_item_db[commons.skip : commons.skip + commons.limit]
    response.update({"Items" : db_items})
    return response

"""Pay attention to the __init__ method used to create the instance of the class:
it has the same parameters as our previous common_parameters:
    "async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):"

Those parameters are what FastAPI will use to "solve" the dependency.

In both cases, it will have:

An optional q query parameter that is a str.
A skip query parameter that is an int, with a default of 0.
A limit query parameter that is an int, with a default of 100.
In both cases the data will be converted, validated, documented on the OpenAPI schema, etc.


Use it¶
Now you can declare your dependency using the class."""

"""FastAPI calls the CommonQueryParams class. This creates an "instance" of that class and the instance will
be passed as the parameter commons to your function."""


"""Type annotation vs Depends¶
Notice how we write CommonQueryParams twice in the above code:

The last CommonQueryParams is what FastAPI will actually use to know what is the dependency.
It is from this one that FastAPI will extract the declared parameters and that is what FastAPI will actually call.

In this case, the first CommonQueryParams doesn't have any special meaning for FastAPI.
FastAPI won't use it for data conversion, validation, etc. (as it is using the Depends(CommonQueryParams) for that).

You could actually write just:
    "commons: Annotated[Any, Depends(CommonQueryParams)]"

    
But declaring the type is encouraged as that way your editor will know what will be passed as the
parameter commons, and then it can help you with code completion, type checks, etc:"""


"""Shortcut¶
But you see that we are having some code repetition here, writing CommonQueryParams twice:
    "commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]"

FastAPI provides a shortcut for these cases, in where the dependency is specifically a class that FastAPI will "call" to create an instance of the class itself.

For those specific cases, you can do the following:

Instead of writing:
    "commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]"
    
you write:
    "commons: Annotated[CommonQueryParams, Depends()]"
    
You declare the dependency as the type of the parameter, and you use Depends() without any parameter,
instead of having to write the full class again inside of Depends(CommonQueryParams)."""



