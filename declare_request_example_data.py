from fastapi import FastAPI
from pydantic import BaseModel

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