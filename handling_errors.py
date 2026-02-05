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