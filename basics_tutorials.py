"""FastAPI is a Python class that provides all the functionality for your API.
FastAPI is a class that inherits directly from Starlette. We can use all the Starlette functionality with FastAPI too."""

from fastapi import FastAPI

"""create a FastAPI "instance. Here the app variable will be an "instance" of the class FastAPI.
This will be the main point of interaction to create all your API."""

app = FastAPI()

"""Now, create a path operation. "Path" here refers to the last part of the URL starting from the first /.

So, in a URL like:
https://example.com/items/foo
...the path would be:
/items/foo

A "path" is also commonly called an "endpoint" or a "route". While building an API, the "path" is the main way
to separate "concerns" and "resources".

Let's see a basic simple code using fastapi that just output the message in
a file as 'Hello World'"""

@app.get("/") # This is called the path operation decorator
async def read_root(): # The read_root() is called the path operation function
    return {"message": "Hello Basics Tutorials"}

"""Operation¶
"Operation" here refers to one of the HTTP "methods".

One of:

POST: to create data.
GET: to read data.
PUT: to update data.
DELETE: to delete data."""

"""Once the code is written, we need to run this file to see the output message.
There are many ways to run a fastapi file. One good method is by typing
below command in any terminal.

Command to run the fastapi based application:
fastapi dev 'file_name.py'. In our case, it is, 'basics_tutorials.py'
So, the actual command is fastapi dev basics_tutorials.py

That 'dev' tells us that the application is in dev mode.

In the output (terminal), there's a line with something like:


INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
That line shows the URL where your app is being served, in your local machine.

Check it¶
Open your browser at http://127.0.0.1:8000.

You will see the JSON response as:

{"message": "Hello World"}"""


"""Interactive API docs¶
Now go to http://127.0.0.1:8000/docs.

You will see the automatic interactive API documentation (provided by Swagger UI):"""
