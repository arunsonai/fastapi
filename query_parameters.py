"""Query Parameters¶
When we declare other function parameters that are not part of the path parameters,
they are automatically interpreted as "query" parameters."""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello Query Parameters!"}

fake_item_id = [{"Item Name": "Foo"}, {"Item Name": "Bar"}, {"Item Name": "Baz"}]

@app.get("/items/")
async def get_items(skip: int = 0, limit: int = 10):
    return fake_item_id[skip : skip + limit]

"""The query is the set of key-value pairs that go after the ? in a URL,
separated by & characters.

For example, in the URL:


http://127.0.0.1:8000/items/?skip=0&limit=10
...the query parameters are:

skip: with a value of 0
limit: with a value of 10"""

"""Defaults¶
As query parameters are not a fixed part of a path, they can be optional
and can have default values.

In the example above they have default values of skip=0 and limit=10.

So, going to the URL:
http://127.0.0.1:8000/items/

would be the same as going to:
http://127.0.0.1:8000/items/?skip=0&limit=10"""

"""Optional parameters¶
The same way, you can declare optional query parameters, by setting their default to None:"""

@app.get("/numbers/{num_id}")
async def get_numbers(num_id: int, q: str | None):
    if q:
        return {"Number ID": num_id, "q" : q}
    else:
        return {"Number ID": num_id}
    
"""Query parameter type conversion¶
You can also declare bool types, and they will be converted:"""

@app.get("/students/{stud_id}")
async def get_students(stud_id: int, stud_name: str | None = None, status: bool = False):
    students = {"Student ID" : stud_id}
    if stud_name != None:
        students.update({"Student Name" : stud_name})
    if not status:
        students.update({"Description" : "This is a lengthy description"})
    return students
"""In the example above, the status query parameter is a bool with a default value of False.
So, if you go to the URL:
http://127.0.0.1:8000/students/1?stud_name=John&status=True
The response will be:
{
  "Student ID": 1,
  "Student Name": "John"
}
If you go to the URL without the status parameter:
http://127.0.0.1:8000/students/1?stud_name=John
The response will be:
{
  "Student ID": 1,
  "Student Name": "John",
  "Description": "This is a lengthy description"
}
If you go to the URL without any query parameters:
http://127.0.0.1:8000/students/1
The response will be:
{
  "Student ID": 1,
  "Description": "This is a lengthy description"
}
http://127.0.0.1:8000/items/foo?status=1 or status=True or status=true or 
status=on or status=ON or status=yes or status=YES will all be interpreted as True.
Otherwise as False."""

"""Multiple path and query parameters¶
You can declare multiple path parameters and query parameters at the same time, FastAPI knows which is which.

And you don't have to declare them in any specific order.

They will be detected by name:"""

@app.get("/schools/{school_id}/area/{area_id}")
async def get_schools(school_id: int, area_id: int, school_name: str | None = None, school_status: bool = True):
    schools = {"School No" : school_id, "Area No" : area_id}
    if school_name is not None:
        schools.update({"School" : school_name})
    if school_status is not True:
        schools.update({"Status" : "Inactive"})
    return schools