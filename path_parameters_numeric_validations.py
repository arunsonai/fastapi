"""Path Parameters and Numeric Validations¶
In the same way that you can declare more validations and metadata for query parameters with Query, you can declare the same type of validations and metadata for path parameters with Path.

Import Path¶
First, import Path from fastapi, and import Annotated:"""


from fastapi import FastAPI, Path, Query
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Path Parameters Numeric Validations"}

@app.get("/pathparams/{item_id}")
async def path_param_valid(item_id: Annotated[int, Path(title='Path Parameters Numeric Validations')],
                           q: Annotated[str | None, Query(min_length=3, max_length=7)] = None):
    results = {"Item ID" : item_id}
    if q:
        results.update({"Query" : q})
    return results

"""Order the parameters as you need¶
Tip

This is probably not as important or necessary if you use Annotated.

Let's say that you want to declare the query parameter q as a required str.

And you don't need to declare anything else for that parameter, so you don't really need to use Query.

But you still need to use Path for the animal_id path parameter. And you don't want to use Annotated for some reason.

Python will complain if you put a value with a "default" before a value that doesn't have a "default".

But you can re-order them, and have the value without a default (the query parameter q) first.

It doesn't matter for FastAPI. It will detect the parameters by their names, types and default
declarations (Query, Path, etc), it doesn't care about the order.

So, you can declare your function as:"""                                                                                                                                                                                                                                                                                                                                                                                                                                                

@app.get("/animals/{animal_id}")
async def get_animals(q : str, animal_id: int = Path(title="Order the Parameters")):
    results = {"Animal ID" : animal_id}
    if q:
        results.update({"Query" : q})
    return results

"""Here's a small trick that can be handy, but you won't need it often.

If you want to:

declare the q query parameter without a Query nor any default value
declare the path parameter item_id using Path
have them in a different order
not use Annotated
...Python has a little special syntax for that.

Pass *, as the first parameter of the function.

Python won't do anything with that *, but it will know that all the following parameters
should be called as keyword arguments (key-value pairs), also known as kwargs. Even if they don't have a default value.
"""

@app.get("/pets/{pet_id}")
async def get_pets(*, pet_id: int = Path(title= "Order Not Matter"), q: str):
    results = {"Pet ID" : pet_id}
    if q:
        results.update({"Query" : q})
    return results

"""Number validations: greater than or equal¶
With Query and Path (and others you'll see later) you can declare number constraints.

Here, with ge=1, item_id will need to be an integer number "greater than or equal" to 1."""

@app.get("/numvals/{num_id}")
async def get_vals(num_id: Annotated[int, Path(title="Number Validations", ge=24)],
                   q: Annotated[str | None, Query(alias="check", min_length=3)] = None):
    results = {"Number ID" : num_id}
    if q:
        results.update({"Query Params" : q})
    return results

"""Number validations: greater than and less than or equal¶
The same applies for:

gt: greater than
le: less than or equal"""

@app.get("/numequals/{num_id}")
async def get_vals(num_id: Annotated[int, Path(title="Number Validations", ge=0, le=1000)],
                   q: Annotated[str | None, Query(alias="check", min_length=3)] = None):
    results = {"Number ID" : num_id}
    if q:
        results.update({"Query Params" : q})
    return results

"""Number validations: floats, greater than and less than¶
Number validations also work for float values.

Here's where it becomes important to be able to declare gt and not just ge.
As with it you can require, for example, that a value must be greater than 0, even if it is less than 1.

So, 0.5 would be a valid value. But 0.0 or 0 would not. And the same for lt."""

@app.get("/numops/{num_id}")
async def get_vals(num_id: Annotated[int, Path(title="Number Validations", ge=0, le=1000)],
                   q: str,
                   size: Annotated[float, Query(gt=0.5, lt=10.99)]):
    results = {"Number ID" : num_id}
    if q:
        results.update({"Query Params" : q})
    if size:
        results.update({"Sizes" : size})
    return results