"""Query Parameters and String Validations¶
FastAPI allows you to declare additional information and validation for your parameters.

Let's take this application as example:

The query parameter q is of type str | None, that means that it's of type str but could also
be None, and indeed, the default value is None, so FastAPI will know it's not required.

Additional validation¶
We are going to enforce that even though q is optional, whenever it is provided, its length doesn't exceed 50 characters.

Import Query and Annotated¶
To achieve that, first import:

1. Query from fastapi
2. Annotated from typing"""

from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Request Body!"}

@app.get("/maxlength/")
async def max_length(q : Annotated[str | None, Query(max_length = 6)] = None):
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"query" : q})
    return results
"""Remember, In the above code, the parameter q is optional because its default value is None. Even if you 
didn't pass any value to it, the endpoint would work without any error."""



"""Add more validations¶
You can also add a parameter min_length:

Adding parameter min_length along with max_length:"""

@app.get("/minlength/")
async def min_length(q : Annotated[str | None, Query(min_length = 3, max_length = 6)] = None):
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"query" : q})
    return results

"""Add regular expressions¶
You can define a regular expression pattern that the parameter should match:"""

@app.get("/regexpressions/")
async def reg_expressions(q : Annotated[str | None, Query(pattern = "^fixedquery$")] = None): 
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"query" : q})
    return results
"""In the above code, pass "http://127.0.0.1:8000/regexpressions/?q=fixedquery" as a value in the URL,
to get the exact answer without any error. The symbol '^' means ''starts with'' and '$' means ''ends with''."""


"""Required parameters¶
When we don't need to declare more validations or metadata, we can make the q query parameter
required just by not declaring a default value, like:
q: str
instead of:
q: str | None = None
But we are now declaring it with Query, for example like:
q: Annotated[str | None, Query(min_length=3)] = None

So, when you need to declare a value as required while using Query, you can simply not declare a default value:"""

@app.get("/required/")
async def min_length(q : Annotated[str, Query(min_length = 3)]):
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"query" : q})
    return results

"""Required, can be None¶
You can declare that a parameter can accept None, but that it's still required. This would force clients to send a value, even if the value is None.

To do that, you can declare that None is a valid type but simply do not declare a default value:
Remember, although it is None type, we need to pass value for q parameter.
Without passing any value for q parameter, it will raise an error.
None type does not mean optional. It just accepts 'None' as a value."""

@app.get("/nonerequired/")
async def none_requierd(q : Annotated[str | None, Query(min_length = 3)]):
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"query" : q})
    return results

"""Query parameter list / multiple values¶
When you define a query parameter explicitly with Query you can also declare it to receive a list of values, or said in another way, to receive multiple values.

For example, to declare a query parameter q that can appear multiple times in the URL, you can write:"""

@app.get("/mulvalues/")
async def mul_values(q : Annotated[list[str] | None, Query()] = None):
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"query" : q})
    return results
"""If we pass below URL in the browser:
http://127.0.0.1:8000/mulvalues/?q=Arun&q=Murugan&q=Gugan

The output would be like:
{"items":[{"item_id":"Foo"},{"item_id":"Bar"}],"query":["Arun","Murugan","Gugan"]}
Remember we should not pass values as ttp://127.0.0.1:8000/mulvalues/?q=Arun, Murugan, Gugan

To declare a query parameter with a type of list, like in the example above, you need to explicitly
use Query, otherwise it would be interpreted as a request body."""



"""Query parameter list / multiple values with defaults¶
You can also define a default list of values if no values are provided:
The q query parameter is optional now. You don't need to provide any value for it. Since the
default value is set to a list of two strings."""

@app.get("/defvalues/")
async def def_values(q : Annotated[list[str] , Query()] = ["Arun", "Murugan"]):
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"query" : q})
    return results

"""if we pass below URL in the browser without any q parameter:
http://127.0.0.1:8000/defvalues/

The output would be like:
{"items":[{"item_id":"Foo"},{"item_id":"Bar"}],"query":["Arun","Murugan"]}"""


"""Declare more metadata¶
You can add more information about the parameter.

That information will be included in the generated OpenAPI and used by the
documentation user interfaces and external tools."""

@app.get("/metadata/")
async def add_data(q : Annotated[str | None, Query(title="Query String",
                                                   description="This is the additional metadata for q parameter")] = None):
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"query" : q})
    return results


"""Alias parameters¶
Imagine that you want the parameter to be item-query.

Like in:
http://127.0.0.1:8000/items/?item-query=foobaritems

But item-query is not a valid Python variable name.

The closest would be item_query.

But you still need it to be exactly item-query...

Then you can declare an alias, and that alias is what will be used to find the parameter value:"""

@app.get("/alias")
async def alias_param(q : Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"query" : q})
    return results

"""You will the same way as before, but now using the alias item-query:
http://127.0.0.1:8001/alias?item-query=Ram

The output would be like:
{"items":[{"item_id":"Foo"},{"item_id":"Bar"}],"query":"Ram"}"""


"""Deprecating parameters¶
Now let's say you don't like this parameter anymore.

You have to leave it there a while because there are clients using it, but you want the docs to clearly show it as deprecated.

Then pass the parameter deprecated=True to Query:"""

@app.get("/deprecated/")
async def dep_params(q : Annotated[str | None, Query(alias="item-query",
                                                     title="Query String",
                                                     description="This is the additional metadata for q parameter",
                                                     deprecated=True)] = None):
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"query" : q})
    return results

"""Exclude parameters from OpenAPI¶
To exclude a query parameter from the generated OpenAPI schema (and thus, from the automatic
documentation systems), set the parameter include_in_schema of Query to False:"""

@app.get("/exparams/")
async def ex_paramas(hidden_params : Annotated[str | None, Query(include_in_schema=False)] = None):
    if hidden_params:
        return {"Hidden Parameters" : hidden_params}
    else:
        return {"Hidden Parameters" : "No data found"}
    
"""Custom Validation¶
There could be cases where you need to do some custom validation that can't be done with the parameters shown above.

In those cases, you can use a custom validator function that is applied after the normal validation (e.g. after validating that the value is a str).

You can achieve that using Pydantic's AfterValidator inside of Annotated.

Note: Pydantic also has BeforeValidator and others."""

import random
from pydantic import AfterValidator

data = {"isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
        "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
        "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2"}

# Below helper function validates whether a given string starts with "isbn-" or "imdb"
def check_validation(id : str):
    if not id.startswith(("isbn-", "imdb")):
        raise ValueError("Data is not in proper format")
    return id

@app.get("/custvalidator/")
async def cust_validator(id: Annotated[str | None, AfterValidator(check_validation)] = None):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"ID" : id, "Value" : item}


