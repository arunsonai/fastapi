from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()
@app.get("/")
async def get_root():
    return {"message" : "Hello Declare Request Example Data"}

"""Declare Request Example Data¶
You can declare examples of the data your app can receive.

Here are several ways to do it.

Extra JSON Schema data in Pydantic models¶
You can declare examples for a Pydantic model that will be added to the generated JSON Schema."""

class DeclareExtraData(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_example_schema" : {
            "examples" : [
                {
                    "name" : "Murugan",
                    "description" : "Yaamiruka Bayam Yen",
                    "price" : 666.66,
                    "tax" : 66.6
                }
            ]
        }
    }

@app.put("/extras/{extra_id}")
async def get_extras(extra_id : int, data: DeclareExtraData):
    results = {"Extra Details" : extra_id, "Extra Data" : data}
    return results

"""Field additional arguments¶
When using Field() with Pydantic models, you can also declare additional examples:"""

class FieldAdditionalArgs(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["All is Well"])
    price: float = Field(examples=[25.38])
    tax: float = Field(default=None, examples=[18.82])

@app.put("/extraexamples/{example}")
async def extra_examples(example : int, addargs: FieldAdditionalArgs):
    results = {"ID" : example, "Additional Arguments" : addargs}
    return results

"""examples in JSON Schema - OpenAPI¶
When using any of:

Path()
Query()
Header()
Cookie()
Body()
Form()
File()
you can also declare a group of examples with additional information that will be added to their JSON Schemas inside of OpenAPI.

Body with examples¶
Here we pass examples containing one example of the data expected in Body():"""

class ExampleJson(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/jsonexample/{example_id}")
async def get_example(
    example_id: int,
    jsondetails: Annotated[ExampleJson,
                           Body(examples=[
                               {
                                   "name" : "Murugan",
                                   "description" : "Name of God",
                                   "price" : 263.85,
                                   "tax" : 18.75
                               }
                           ]

        )
    ]
):
    results = {"Example ID" : example_id, "JSON Details" : jsondetails}
    return results

"""Body with multiple examples¶
You can of course also pass multiple examples:"""

@app.put("/mulexamples/{example_id}")
async def mul_examples(example_id: int,
                       jsonexample: Annotated[ExampleJson,
                                              Body(examples=[
                                                  {
                                                      "name" : "Arumugam",
                                                      "description" : "One Name of Lord Murugan",
                                                      "price" : 66.6,
                                                      "tax" : 6.6
                                                  },
                                                  {
                                                       "name" : "Velan",
                                                       "description" : "Another name of Lord Murugan",
                                                       "price" : 6.66,
                                                       "tax" : 6.66
                                                  },
                                                  {
                                                       "name" : "Kathirvelan",
                                                       "description" : "Different Name of Lord Murugan",
                                                       "price" : 666.66,
                                                       "tax" : 66.6
                                                  }
                                              ]
                                                  
                                              )
                           
                       ] 

):
    results = {"Example ID" : example_id, "Multiple Examples" : jsonexample}
    return results