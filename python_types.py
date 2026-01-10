"""Python has support for optional "type hints" (also called "type annotations").

These "type hints" or annotations are a special syntax that allow declaring the type of a variable.

By declaring types for your variables, editors and tools can give you better support.

Let's use the Python's default type hints that is available ver> 3.9
This helps to understand the type of variables, function arguments, return statements etc."""

def my_name(user: str) -> str:
    return user.title()

my_name("arun kumar")

"""The above code is not the same as declaring default values like would be with:
first_name="john", last_name="doe"
It's a different thing.

We are using colons (:), not equals (=).

And adding type hints normally doesn't change what happens from what would happen without them."""

# Below code will not help you with dot (.) parameters if you don't use type hints.
# The beauty of type hints is that editors and tools can use them to give you better support.
def get_full_name(first_name: str, last_name: str) -> str:
    full_name = first_name.title() + " " + last_name.title()
    return full_name

get_full_name("arun", "kumar")

"""Simple types¶
You can declare all the standard Python types, not only str.

You can use, for example:

* int
* float
* bool
* bytes"""

def get_all_data(name: str, age: int, weight: float, married: bool, data: bytes):
    print(name, age, weight, married, data)

get_all_data("Arun", 30, 75.5, True, b"sample data")

"""Generic types with type parameters¶
There are some data structures that can contain other values, like dict, list, set and tuple.
And the internal values can have their own type too.

These types that have internal types are called "generic" types.
And it's possible to declare them, even with their internal types.
Examples of Generic types are: list, dict, set, tuple etc.
"""
# Below are some examples of Generic types with type parameters.
# The variable 'arg_item' is a variable with 'list' generic type and 'str' type parameter.
# The 'arg_item' declared as a list of strings (list[str]).
def get_list_items(arg_item: list[str]):
    for item in arg_item:
        print("Item:", item)

get_list_items(["apple", "banana", "cherry"])

"""Tuple and Set¶
You would do the same to declare tuples and sets:
"""

def get_name_age(name: tuple[int, int, str], age: set[int, int]):
    print(name, age)

"""This means:

The variable name is a tuple with 3 items, an int, another int, and a str.
The variable age is a set, and each of its items is of type int"""

get_name_age(name=(20, 90, 45), age={30, 31})

"""Dict¶
To define a dict, you pass 2 type parameters, separated by commas.

The first type parameter is for the keys of the dict.

The second type parameter is for the values of the dict"""

def get_age_details(age: dict[str, int]):
    for name, age_value in age.items():
        print(f"The age of {name} is {age_value}")

"""This means:

The variable age is a dict:
The keys of this dict are of type str (let's say, the name of each item).
The values of this dict are of type int (let's say, the age of each item)."""

get_age_details({"delson":30, "Gugan":1})

"""Union¶
You can declare that a variable can be any of several types, for example, an int or a str.

In Python 3.6 and above (including Python 3.10) we can use the Union type from typing and 
put inside the square brackets the possible types to accept.

In Python 3.10 there's also a new syntax where you can put the possible types separated
by a vertical bar (|)."""

def check_output(name: str | None):
    if name:
        print(f"Name is provided: {name}")
    else:
        print("No name provided")

check_output(None)

"""Classes as types¶
You can also declare a class as the type of a variable.

Let's say you have a class Person, with a name:"""

class Person:
    def __init__(self, name:str):
        self.name = name

def get_person(one_name: Person):
    print(f"The name of the person is {one_name.name}")

get_person(Person("Alice"))

"""Environment Variables

An environment variable (also known as "env var") is a variable that lives outside of the 
Python code, in the operating system, and could be read by your Python code (or by other 
programs as well).

Environment variables could be useful for handling application settings, as part 
of the installation of Python, etc.

Create and Use Env Vars¶
We can create environment variables in Windows machine by typing edit environment variables
in the Start Menu search box.
Goto Advanced tab and click on Environment Variables button.
Add a new user variable MY_NAME with value as your name.
Once added, close VS Code (or any other editor) and re-open it to make sure
the env var is picked up."""

# Below code reads the env var MY_NAME and prints it. os module need to be imported.
import os
name = os.getenv("MY_NAME")
if name:
    print(f"Hello {name}")
else:
    print(f"Hello World!")