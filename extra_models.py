from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Extra Models"}

"""Extra Models¶
Continuing with the previous example, it will be common to have more than one related model.

This is especially the case for user models, because:

The input model needs to be able to have a password.
The output model should not have a password.
The database model would probably need to have a hashed password."""

"""Multiple models¶
Here's a general idea of how the models could look like with their password fields and the places where they are used:"""

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
     username: str
     email: EmailStr
     full_name: str | None = None

class UserInDb(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None

def fake_password_hasher(raw_password: str):
    return "supersecret " + raw_password

def fake_save_user(user_in: UserIn):
    hash_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDb(**user_in.model_dump, hashed_password=hash_password)
    print("User Saved successfully")
    return user_in_db

@app.get("/userdetails/", response_model=UserOut)
async def get_details(user_in: UserIn):
    result = fake_save_user(user_in)
    return result


"""Reduce duplication¶
Reducing code duplication is one of the core ideas in FastAPI.

As code duplication increments the chances of bugs, security issues, code desynchronization
issues (when you update in one place but not in the others), etc.

And these models are all sharing a lot of the data and duplicating attribute names and types.

We could do better.

We can declare a UserBase model that serves as a base for our other models. And then we can make subclasses
of that model that inherit its attributes (type declarations, validation, etc).

All the data conversion, validation, documentation, etc. will still work as normally.

That way, we can declare just the differences between the models (with plaintext password,
with hashed_password and without password):
"""

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

def get_raw_password(raw_password: str):
    return "supersecret " + raw_password

def get_hashed_password(user_in: UserIn):
    raw_password = get_raw_password(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password= raw_password)
    print("Password set successfully")
    return user_in_db

@app.post("/users/", response_model=UserOut)
async def get_users(user: UserIn):
    get_user_details = get_hashed_password(user)
    return get_user_details


"""Union or anyOf¶
You can declare a response to be the Union of two or more types, that means, that the response would be any of them.

It will be defined in OpenAPI with anyOf.

To do that, use the standard Python type hint typing.Union:

Note

When defining a Union, include the most specific type first, followed by the less specific type.
In the example below, the more specific PlaneItem comes before CarItem in Union[PlaneItem, CarItem]."""

class BaseItem(BaseModel):
    description: str | None = None
    type: str

class CarItem(BaseItem):
    type: str

class PlaneItem(BaseItem):
    type: str
    size: float = 10.5

items = {
    "foo" : {"description" : "This a car type", "type" : "car"},
    "bar" : {"description": "This is a plane", "type" : "plane", "size" : 66.66666}
}

@app.post("/vehicles/{vehicle_id}", response_model= PlaneItem | CarItem)
async def get_vehicle_details(vehicle_id: str):
    return items[vehicle_id]


"""Union in Python 3.10¶
In this example we pass Union[PlaneItem, CarItem] as the value of the argument response_model.

Because we are passing it as a value to an argument instead of putting it in a type annotation, we have to use Union even in Python 3.10.

If it was in a type annotation we could have used the vertical bar, as:


some_variable: PlaneItem | CarItem
But if we put that in the assignment response_model=PlaneItem | CarItem we would get an error, because
Python would try to perform an invalid operation between PlaneItem and CarItem instead of interpreting that as a type annotation."""


"""List of models¶
The same way, you can declare responses of lists of objects.

For that, use the standard Python typing.List (or just list in Python 3.9 and above):"""

class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


@app.get("/items/", response_model=list[Item])
async def read_items():
    return items

"""Response with arbitrary dict¶
You can also declare a response using a plain arbitrary dict, declaring just the type of the keys and values,
without using a Pydantic model.

This is useful if you don't know the valid field/attribute names (that would be needed for a Pydantic model) beforehand.

In this case, you can use typing.Dict (or just dict in Python 3.9 and above):"""

@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}


