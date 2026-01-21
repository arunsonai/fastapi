"""Header Parameters¶
You can define Header parameters the same way you define Query, Path and Cookie parameters.

Import Header¶
First import Header:"""

from fastapi import FastAPI, Header
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Header Parameters"}

@app.get("/headerparam/")
async def get_header(user_agent: Annotated[str | None, Header()] = None):
    return {"Header Details" : user_agent}
"""In Swagger UI, if you pass the value for the variable 'user_agent' as 'Shanmugar' you will get the response body as below.

Response body
Download
{
  "Header Details": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
The reason for not getting the value as 'Shanmugar' is because it is semantically special.
FastAPI is automatically mapping your variable name to an HTTP header. Browsers always send it.

Try with different HTTP header like User-Agent Accept, Content-Type, Authorization,
Host, Accept-Encoding, Accept-Language, Cache-Control, Connection, Referer and see the magical output"""

"""Automatic conversion¶
Header has a little extra functionality on top of what Path, Query and Cookie provide.

Most of the standard headers are separated by a "hyphen" character, also known as the "minus symbol" (-).

But a variable like user-agent is invalid in Python.

So, by default, Header will convert the parameter names characters from
underscore (_) to hyphen (-) to extract and document the headers.

Also, HTTP headers are case-insensitive, so, you can declare them with standard
Python style (also known as "snake_case").

So, you can use user_agent as you normally would in Python code, instead of
needing to capitalize the first letters as User_Agent or something similar.

If for some reason you need to disable automatic conversion of underscores to hyphens,
set the parameter convert_underscores of Header to False:"""


@app.get("/items/")
async def get_items(strange_header: Annotated[str | None, Header(convert_underscores=False)] = None):
    return {"Strange Headers" : strange_header}

"""Duplicate headers¶
It is possible to receive duplicate headers. That means, the same header with multiple values.

You can define those cases using a list in the type declaration.

You will receive all the values from the duplicate header as a Python list.

For example, to declare a header of X-Token that can appear more than once, you can write:"""

@app.get("/dupheader/")
async def dup_header(many_headers: Annotated[list[str] | None, Header()] = None):
    return {"Duplicate Headers" : many_headers}

