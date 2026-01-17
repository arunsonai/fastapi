"""The same way you can declare additional validation and metadata in path operation function parameters with Query, Path and Body, you can declare validation and metadata inside of Pydantic models using Pydantic's Field.

Import Field¶
First, you have to import it:"""

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message":"Hello Body Fields!"}

class Materials(BaseModel):
    subject: str | None = Field(default=None, alias="sub")
    syllabus: str = Field(title="Final Year Syllabus",
                          description="This is a syllabus for Final Year Students",
                          min_length=5, max_length=50)
    department: int = Field(title="Departments", gt=5, le=20)

@app.put("/books/{book_id}")
async def get_books(book_id: int,
                    details: Materials):
    return {"Books" : book_id, "Book Details" : details}