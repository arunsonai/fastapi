from fastapi import FastAPI, HTTPException

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