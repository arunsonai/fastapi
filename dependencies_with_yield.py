"""Dependencies with yield¶
FastAPI supports dependencies that do some extra steps after finishing.

To do this, use yield instead of return, and write the extra steps (code) after.

Tip: Make sure to use yield one single time per dependency.

Any function that is valid to use with:

@contextlib.contextmanager or
@contextlib.asynccontextmanager
would be valid to use as a FastAPI dependency.

In fact, FastAPI uses those two decorators internally."""


from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Dependencies with yield!"}

"""A database dependency with yield¶
For example, you could use this to create a database session and close it after finishing.

Only the code prior to and including the yield statement is executed before creating a response:"""

def DBSession():
    pass

async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

"""A dependency with yield and try¶
If you use a try block in a dependency with yield, you'll receive any exception that was thrown when using the dependency.

For example, if some code at some point in the middle, in another dependency or in a path operation, made a
database transaction "rollback" or created any other exception, you would receive the exception in your dependency.

So, you can look for that specific exception inside the dependency with except SomeException.

In the same way, you can use finally to make sure the exit steps are executed, no matter if there was an exception or not."""


"""Sub-dependencies with yield¶
You can have sub-dependencies and "trees" of sub-dependencies of any size and shape, and any or all of them can use yield.

FastAPI will make sure that the "exit code" in each dependency with yield is run in the correct order.

For example, dependency_c can have a dependency on dependency_b, and dependency_b on dependency_a:"""

def generate_dep_a():
    pass


async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a: Annotated[DepA, Depends(dependency_a)]):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b: Annotated[DepB, Depends(dependency_b)]):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)