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
async def path_param_valid(item_id : Annotated[int, Path(title='Path Parameters Numeric Validations')],
                           q : Annotated[str | None, Query(min_length=3, max_length=7)] = None):
    results = {"Item ID" : item_id}
    if q:
        results.update({"Query" : q})
    return results

"""Declare metadata¶
You can declare all the same parameters as for Query.

For example, to declare a title metadata value for the path parameter item_id you can type:"""