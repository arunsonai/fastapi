"""Request Forms and Files¶
You can define files and form fields at the same time using File and Form."""


from fastapi import FastAPI, File, Form, UploadFile
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Request Files and Forms"}


@app.post("/filesandforms/")
async def get_files_forms(param_forms: Annotated[str, Form()],
                          param_files: Annotated[bytes, File()],
                          param_upload_files: Annotated[UploadFile, File()]
                          ):
    return {
        "Form Details" : param_forms,
        "File Size" : len(param_files),
        "File Format" : param_upload_files.content_type
    }

"""The files and form fields will be uploaded as form data and you will receive the files and form fields.

And you can declare some of the files as bytes and some as UploadFile.

Warning:

You can declare multiple File and Form parameters in a path operation, but you can't also declare
Body fields that you expect to receive as JSON, as the request will have the body encoded
using multipart/form-data instead of application/json.

This is not a limitation of FastAPI, it's part of the HTTP protocol."""