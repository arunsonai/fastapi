from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Body Nested Models"}

"""Body - Nested Models¶
With FastAPI, you can define, validate, document, and use arbitrarily deeply nested models (thanks to Pydantic).

List fields¶
You can define an attribute to be a subtype. For example, a Python list:"""

class Tables(BaseModel):
    design: int | None = None
    size: float
    structure: list = []

@app.put("/chairs/{chair_id}")
async def get_tables(chair_id: int, table: Tables):
    results = {"Chair Details" : chair_id, "Table Details" : table}
    return results

"""This will make 'structure' be a list, although it doesn't declare the type of the elements of the list.

List fields with type parameter¶
But Python has a specific way to declare lists with internal types, or "type parameters":

Declare a list with a type parameter¶
To declare types that have type parameters (internal types), like list, dict, tuple,
pass the internal type(s) as "type parameters" using square brackets: [ and ]


my_list: list[str]
That's all standard Python syntax for type declarations.

Use that same standard syntax for model attributes with internal types.

So, in our example, we can make 'structure' be specifically a "list of strings":"""

class FModifiedTables(BaseModel):
    design: int | None = None
    size: float
    structure: list[str] = []

@app.put("/fmodtables/{chair_id}")
async def fmod_tables(chair_id: int, table: Tables):
    results = {"Chair Details" : chair_id, "Table Details" : table}
    return results

"""Set types¶
But then we think about it, and realize that tags shouldn't repeat, they would probably be unique strings.

And Python has a special data type for sets of unique items, the set.

Then we can declare tags as a set of strings:"""

class SModTables(BaseModel):
    design: int | None = None
    size: float
    structure: set[str] = set()

@app.put("/smodtables/{chair_id}")
async def smod_tables(chair_id: int, table: Tables):
    results = {"Chair Details" : chair_id, "Table Details" : table}
    return results

"""With this, even if you receive a request with duplicate data, it will be converted to a set of unique items.

And whenever you output that data, even if the source had duplicates, it will be output as a set of unique items.

And it will be annotated / documented accordingly too."""


"""Nested Models¶
Each attribute of a Pydantic model has a type.

But that type can itself be another Pydantic model.

So, you can declare deeply nested JSON "objects" with specific attribute names, types and validations.

All that, arbitrarily nested.

Define a submodel¶
For example, we can define an Image model:"""

class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float
    tags: set[str] = set()
    image: Image | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    results = {"Item_ID" : item_id, "Item Details" : item}
    return results

"""Special types and validation¶
Apart from normal singular types like str, int, float, etc. you can use more complex singular types that inherit from str.

For example, as in the Image model we have a url field, we can declare it to be an instance of Pydantic's HttpUrl instead of a str:"""

class ModImage(BaseModel):
    url: HttpUrl # complex singular types that inherit from str
    name: str

class ModItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float
    tags: set[str] = set()
    image: ModImage | None = None

@app.put("/moditems/{item_id}")
async def mod_update_item(item_id: int, mod_item: ModItem):
    results = {"Item ID" : item_id, "Mod Item" : mod_item}
    return results

"""Attributes with lists of submodels¶
You can also use Pydantic models as subtypes of list, set, etc.:"""

class SModItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float
    tags: set[str] = set()
    image: list[ModImage] | None = None

@app.put("/Smoditems/{item_id}")
async def smod_update_item(item_id: int, smod_item: SModItem):
    results = {"Modified Item" : smod_update_item, "Item Details" : smod_item}
    return results

"""You can see the output as Request Body & Response Body
Request Body:
{
  "name": "Murugan",
  "description": "This is a desc",
  "price": 25.92,
  "tax": 18.20,
  "tags": ["Arun", "Velan", "Vetrivel"],
  "image": [
    {
      "url": "https://facebook.com/",
      "name": "Facebook"
    },
    {
      "url": "https://twitter.com/",
      "name": "Twitter_Old"
    },
    {
      "url": "https://x.com/",
      "name": "Twitter_New"
    }
  ]
}
Response Body:

{
  "Modified Item": {},
  "Item Details": {
    "name": "Murugan",
    "description": "This is a desc",
    "price": 25.92,
    "tax": 18.2,
    "tags": [
      "Arun",
      "Vetrivel",
      "Velan"
    ],
    "image": [
      {
        "url": "https://facebook.com/",
        "name": "Facebook"
      },
      {
        "url": "https://twitter.com/",
        "name": "Twitter_Old"
      },
      {
        "url": "https://x.com/",
        "name": "Twitter_New"
      }
    ]
  }
}
"""

"""Deeply nested models¶
You can define arbitrarily deeply nested models:

"""

class TModImage(BaseModel):
    url : HttpUrl
    name : str

class TModItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float
    tags: set[str] = set()
    image: list[TModImage] | None = None

class Offer(BaseModel):
    name: str
    description: str | None = None
    items : list[TModItem]

@app.post("/order/")
async def create_item(offer : Offer):
    return offer

"""The output of the request body & response body would be
Request Body:
{
  "name": "SevalKodiVeeran",
  "description": "Yaamiruka Bayam Yen",
  "items": [
    {
      "name": "Shanmugar",
      "description": "Murugar Padai Veedu",
      "price": 389.99,
      "tax": 18.4,
      "tags": ["Velan", "Senthuran", "Rawoothar"],
      "image": [
        {
          "url": "https://instagram.com/",
          "name": "Instagram"
        },
        {
          "url": "https://facebook.com/",
          "name": "FaceBook"
        },
        {
          "url": "https://twitter.com/",
          "name": "Twitter"
        },
        {
          "url": "https://whatsapp.com/",
          "name": "Whatsapp"
        }
      ]
    },
   {
      "name": "SenthilNathar",
      "description": "Irandam Padai Veedu",
      "price": 66.66,
      "tax": 16.6,
      "tags": ["Arumugan", "Kathirvelan", "Namasivayan"],
      "image": [
        {
          "url": "https://x.com/",
          "name": "X"
        },
        {
          "url": "https://flipkart.com/",
          "name": "Flipkart"
        },
        {
          "url": "https://amazon.in/",
          "name": "Amazon"
        },
        {
          "url": "https://meeshow.com/",
          "name": "Meeshow"
        }
      ]
    },
   {
      "name": "Palaniandavar",
      "description": "Moondram Padai Veedu",
      "price": 333.99,
      "tax": 39.9,
      "tags": ["Palani", "Idumbayudhan", "Thiruvavinankudi"],
      "image": [
        {
          "url": "https://mavel.com/",
          "name": "Mavel"
        },
        {
          "url": "https://namasivaya.com/",
          "name": "NamaShivaya"
        },
        {
          "url": "https://sadaksharan.com/",
          "name": "Sadaksharan"
        },
        {
          "url": "https://vel.com/",
          "name": "Vel"
        }
      ]
    }
  ]
}

Response Body:
{
  "name": "SevalKodiVeeran",
  "description": "Yaamiruka Bayam Yen",
  "items": [
    {
      "name": "Shanmugar",
      "description": "Murugar Padai Veedu",
      "price": 389.99,
      "tax": 18.4,
      "tags": [
        "Velan",
        "Senthuran",
        "Rawoothar"
      ],
      "image": [
        {
          "url": "https://instagram.com/",
          "name": "Instagram"
        },
        {
          "url": "https://facebook.com/",
          "name": "FaceBook"
        },
        {
          "url": "https://twitter.com/",
          "name": "Twitter"
        },
        {
          "url": "https://whatsapp.com/",
          "name": "Whatsapp"
        }
      ]
    },
    {
      "name": "SenthilNathar",
      "description": "Irandam Padai Veedu",
      "price": 66.66,
      "tax": 16.6,
      "tags": [
        "Kathirvelan",
        "Namasivayan",
        "Arumugan"
      ],
      "image": [
        {
          "url": "https://x.com/",
          "name": "X"
        },
        {
          "url": "https://flipkart.com/",
          "name": "Flipkart"
        },
        {
          "url": "https://amazon.in/",
          "name": "Amazon"
        },
        {
          "url": "https://meeshow.com/",
          "name": "Meeshow"
        }
      ]
    },
    {
      "name": "Palaniandavar",
      "description": "Moondram Padai Veedu",
      "price": 333.99,
      "tax": 39.9,
      "tags": [
        "Idumbayudhan",
        "Thiruvavinankudi",
        "Palani"
      ],
      "image": [
        {
          "url": "https://mavel.com/",
          "name": "Mavel"
        },
        {
          "url": "https://namasivaya.com/",
          "name": "NamaShivaya"
        },
        {
          "url": "https://sadaksharan.com/",
          "name": "Sadaksharan"
        },
        {
          "url": "https://vel.com/",
          "name": "Vel"
        }
      ]
    }
  ]
}"""


"""Bodies of pure lists¶
If the top level value of the JSON body you expect is a JSON array (a Python list),
you can declare the type in the parameter of the function, the same as in Pydantic models:"""

@app.post("/images/{multiple}")
async def get_images(fimage: list[ModImage]):
    return fimage

"""Bodies of arbitrary dicts¶
You can also declare a body as a dict with keys of some type and values of some other type.

This way, you don't have to know beforehand what the valid field/attribute names are (as would be the case with Pydantic models).

This would be useful if you want to receive keys that you don't already know.

Another useful case is when you want to have keys of another type (e.g., int).

That's what we are going to see here.

In this case, you would accept any dict as long as it has int keys with float values:"""

@app.post("/arbitdict/")
async def any_values(weights: dict[int, float]):
    return weights

"""The output of Swagger UI with URL, Request Body, Response Body are below

Request URL:
http://127.0.0.1:8001/arbitdict/

Request Body:
{
  "1726": 78.95,
  "7892": 121.7,
  "5270": 45.38
}

Response Body:
{
  "1726": 78.95,
  "5270": 45.38,
  "7892": 121.7
}
"""