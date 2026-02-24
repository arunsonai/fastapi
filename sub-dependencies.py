from fastapi import FastAPI, Cookie, Depends
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Sub-Dependencies!"}

"""Sub-dependencies¶
You can create dependencies that have sub-dependencies.

They can be as deep as you need them to be.

FastAPI will take care of solving them.

First dependency "dependable"¶
You could create a first dependency ("dependable") like:"""

#First dependency or dependable
async def query_extractor(q: str | None = None):
    return q

"""It declares an optional query parameter q as a str, and then it just returns it.

This is quite simple (not very useful), but will help us focus on how the sub-dependencies work."""



"""Second dependency, "dependable" and "dependant"¶
Then you can create another dependency function (a "dependable") that at the same time declares a dependency
of its own (so it is a "dependant" too):"""

# Second dependency or dependable
# Remember to import Cookie & Depends from fastapi
async def query_or_cookie_extractor(q: Annotated[str, Depends(query_extractor)],
                                    last_query: Annotated[str | None , Cookie()] = None):
    if not q:
        return last_query
    return q

"""Let's focus on the parameters declared:

Even though this function is a dependency ("dependable") itself, it also declares another dependency (it "depends" on something else).
It depends on the query_extractor, and assigns the value returned by it to the parameter q.
It also declares an optional last_query cookie, as a str.
If the user didn't provide any query q, we use the last query used, which we saved to a cookie before.""" 


"""Use the dependency¶
Then we can use the dependency with:"""

@app.get("/items/")
async def get_items(query_or_default: Annotated[str | None, Depends(query_or_cookie_extractor)]):
    return {"Details" : query_or_default}