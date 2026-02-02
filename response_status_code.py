from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Response Status Code"}

@app.post("/status/", status_code=201)
async def get_status(name: str):
    return {"Name" : name}

"""Some response codes (see the next section) indicate that the response does not have a body.

FastAPI knows this, and will produce OpenAPI docs that state there is no response body."""


"""About HTTP status codes¶

In HTTP, you send a numeric status code of 3 digits as part of the response.

These status codes have a name associated to recognize them, but the important part is the number.

In short:

100 - 199 are for "Information". You rarely use them directly. Responses with these status codes cannot have a body.
200 - 299 are for "Successful" responses. These are the ones you would use the most.
200 is the default status code, which means everything was "OK".
Another example would be 201, "Created". It is commonly used after creating a new record in the database.
A special case is 204, "No Content". This response is used when there is no content to return to the client, and
so the response must not have a body.
300 - 399 are for "Redirection". Responses with these status codes may or may not have a body, except
for 304, "Not Modified", which must not have one.
400 - 499 are for "Client error" responses. These are the second type you would probably use the most.
An example is 404, for a "Not Found" response.
For generic errors from the client, you can just use 400.
500 - 599 are for server errors. You almost never use them directly. When something goes wrong at some part
in your application code, or server, it will automatically return one of these status codes."""


# Remember to import 'status' module from fastapi
@app.post("/information/", status_code=status.HTTP_201_CREATED)
async def create_item(full_name: str):
    return {"Details" : full_name}