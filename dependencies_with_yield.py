"""Dependencies with yield¶
FastAPI supports dependencies that do some extra steps after finishing.

To do this, use yield instead of return, and write the extra steps (code) after.

Tip: Make sure to use yield one single time per dependency.

Any function that is valid to use with:

@contextlib.contextmanager or
@contextlib.asynccontextmanager
would be valid to use as a FastAPI dependency.

In fact, FastAPI uses those two decorators internally."""


from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Dependencies with yield!"}

"""A database dependency with yield¶
For example, you could use this to create a database session and close it after finishing.

Only the code prior to and including the yield statement is executed before creating a response:"""

async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()