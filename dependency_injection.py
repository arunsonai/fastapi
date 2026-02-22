"""Dependencies¶
FastAPI has a very powerful but intuitive Dependency Injection system.

It is designed to be very simple to use, and to make it very easy for any developer to integrate other components with FastAPI.

What is "Dependency Injection"¶
"Dependency Injection" means, in programming, that there is a way for your code (in this case, your path operation functions)
to declare things that it requires to work and use: "dependencies".

And then, that system (in this case FastAPI) will take care of doing whatever is needed to provide your code
with those needed dependencies ("inject" the dependencies).

This is very useful when you need to:

1. Have shared logic (the same code logic again and again).
2. Share database connections.
3. Enforce security, authentication, role requirements, etc.
    And many other things...
All these, while minimizing code repetition.

First Steps¶
Let's see a very simple example. It will be so simple that it is not very useful, for now.

But this way we can focus on how the Dependency Injection system works.

Create a dependency, or "dependable"¶
Let's first focus on the dependency.

It is just a function that can take all the same parameters that a path operation function can take:
"""


from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Dependency injection!"}

def get_details(q : str, price: int=20, tax: float=66.6666):
    return {"Quantity" : q, "Price Value" : price, "Tax Value" : tax}


@app.get("/items/")
async def get_items(commons: Annotated[dict, Depends(get_details)]):
    return commons

@app.get("/total/")
async def get_total(similar: Annotated[dict, Depends(get_details)]):
    return similar

""""Share Annotated dependencies¶
In the examples above, you see that there's a tiny bit of code duplication.

When you need to use the common_parameters() dependency, you have to write the whole parameter with the type annotation and Depends():


commons: Annotated[dict, Depends(common_parameters)]
But because we are using Annotated, we can store that Annotated value in a variable and use it in multiple places:"""

common_place = Annotated[dict, Depends(get_details)]

@app.get("/stores/")
async def get_values(groups: common_place):
    return groups

"""The dependencies will keep working as expected, and the best part is that the type information will be preserved,
which means that your editor will be able to keep providing you with autocompletion, inline errors, etc.
The same for other tools like mypy.

This will be especially useful when you use it in a large code base where you use the same dependencies
over and over again in many path operations."""


"""To async or not to async¶
As dependencies will also be called by FastAPI (the same as your path operation functions), the same
rules apply while defining your functions.

You can use async def or normal def.

And you can declare dependencies with async def inside of normal def path operation functions, or def dependencies
inside of async def path operation functions, etc.

It doesn't matter. FastAPI will know what to do."""


"""Integrated with OpenAPI¶
All the request declarations, validations and requirements of your dependencies (and sub-dependencies) will be
integrated in the same OpenAPI schema.

So, the interactive docs will have all the information from these dependencies too"""


"""Simple usage¶
If you look at it, path operation functions are declared to be used whenever a path and operation matches,
and then FastAPI takes care of calling the function with the correct parameters, extracting the data from the request.

Actually, all (or most) of the web frameworks work in this same way.

You never call those functions directly. They are called by your framework (in this case, FastAPI).

With the Dependency Injection system, you can also tell FastAPI that your path operation function also "depends" on
something else that should be executed before your path operation function, and FastAPI will take care of executing
it and "injecting" the results.

Other common terms for this same idea of "dependency injection" are:

resources
providers
services
injectables
components
"""

"""FastAPI plug-ins¶
Integrations and "plug-ins" can be built using the Dependency Injection system. But in fact, there is actually
no need to create "plug-ins", as by using dependencies it's possible to declare an infinite number of integrations
and interactions that become available to your path operation functions.

And dependencies can be created in a very simple and intuitive way that allows you to just import the Python packages
you need, and integrate them with your API functions in a couple of lines of code, literally.

You will see examples of this in the next chapters, about relational and NoSQL databases, security, etc."""

"""FastAPI compatibility¶
The simplicity of the dependency injection system makes FastAPI compatible with:

all the relational databases
NoSQL databases
external packages
external APIs
authentication and authorization systems
API usage monitoring systems
response data injection systems
etc."""


"""Simple and Powerful¶
Although the hierarchical dependency injection system is very simple to define and use, it's still very powerful.

You can define dependencies that in turn can define dependencies themselves.

In the end, a hierarchical tree of dependencies is built, and the Dependency Injection system takes care of
solving all these dependencies for you (and their sub-dependencies) and providing (injecting) the results at each step.

For example, let's say you have 4 API endpoints (path operations):

/items/public/
/items/private/
/users/{user_id}/activate
/items/pro/
then you could add different permission requirements for each of them just with dependencies and sub-dependencies:"""


"""Integrated with OpenAPI¶
All these dependencies, while declaring their requirements, also add parameters, validations, etc. to your path operations.

FastAPI will take care of adding it all to the OpenAPI schema, so that it is shown in the interactive documentation systems."""