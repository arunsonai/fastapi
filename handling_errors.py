from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Handling Errors!"}

items = {"Foo" : "It is an item in Foo"}
@app.get("/users/{user_id}")
async def get_users(user_id: str):
    if user_id not in items:
        raise HTTPException(status_code=404, detail="Information not available")
    return items[user_id]

"""Add custom headers¶
There are some situations in where it's useful to be able to add custom headers to the HTTP error.
For example, for some types of security.

You probably won't need to use it directly in your code.

But in case you needed it for an advanced scenario, you can add custom headers:"""

@app.get("/addheaders/{item_id}")
async def add_headers(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error" : "There goes my error"}
        )
    return {"Item Details" : items[item_id]}

"""Install custom exception handlers¶
You can add custom exception handlers with the same exception utilities from Starlette.

Let's say you have a custom exception UnicornException that you (or a library you use) might raise.

And you want to handle this exception globally with FastAPI.

You could add a custom exception handler with @app.exception_handler():"""

class Unicorn_Exception(Exception):
    def __init__(self, name):
        self.name = name

# Remember to import 'Request' from fastapi and 'JSONRespinse' from 'fastapi.requests'
@app.exception_handler(Unicorn_Exception)
async def unicorn_exception_handler(request: Request, exc: Unicorn_Exception):
    return JSONResponse(
        status_code=418,
        content={"message" : f"The {exc.name} done something wrong!"}
    )

@app.get("/exceptions/{name}")
async def get_exception(name: str):
    if name == "soorabadhman":
        raise Unicorn_Exception(name=name)
    return {"Unicorn_Name" : name}


"""Override the default exception handlers¶
FastAPI has some default exception handlers.

These handlers are in charge of returning the default JSON responses when you raise an HTTPException and when the request has invalid data.

You can override these exception handlers with your own.


Override request validation exceptions¶
When a request contains invalid data, FastAPI internally raises a RequestValidationError.

And it also includes a default exception handler for it.

To override it, import the RequestValidationError and use it with @app.exception_handler(RequestValidationError) to decorate the exception handler.

The exception handler will receive a Request and the exception.
"""

@app.exception_handler(RequestValidationError)
async def HTTP_Validation_Error(request, exc):
    return PlainTextResponse(str(exc.detail), status_code = exc.status_code)

@app.
