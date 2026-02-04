"""Request Files¶
You can define files to be uploaded by the client using File."""


from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from typing import Annotated

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message" : "Hello Request Files"}


"""Define File Parameters¶
Create file parameters the same way you would for Body or Form"""

# Remember to import 'File' and 'UploadFile' from fastapi
@app.post("/files/")
async def get_file(param_file: Annotated[bytes, File()]):
    return len(param_file)

"""The files will be uploaded as "form data".

If you declare the type of your path operation function parameter as bytes, FastAPI will read
the file for you and you will receive the contents as bytes.

Keep in mind that this means that the whole contents will be stored in memory. This will work well for small files.

But there are several cases in which you might benefit from using UploadFile"""

"""File Parameters with UploadFile¶
Define a file parameter with a type of UploadFile"""

@app.post("/documents/")
async def get_data(param_data: UploadFile):
    return param_data.filename

"""Using UploadFile has several advantages over bytes:

You don't have to use File() in the default value of the parameter.
It uses a "spooled" file:
A file stored in memory up to a maximum size limit, and after passing this limit it will be stored in disk.
This means that it will work well for large files like images, videos, large binaries, etc. without consuming all the memory.
You can get metadata from the uploaded file.
It has a file-like async interface.
It exposes an actual Python SpooledTemporaryFile object that you can pass directly to other libraries that expect a file-like object."""



"""UploadFile¶
UploadFile has the following attributes:

filename: A str with the original file name that was uploaded (e.g. myimage.jpg).

content_type: A str with the content type (MIME type / media type) (e.g. image/jpeg).

file: A SpooledTemporaryFile (a file-like object). This is the actual Python file object that you can pass
directly to other functions or libraries that expect a "file-like" object."""



"""UploadFile has the following async methods. They all call the corresponding file methods
underneath (using the internal SpooledTemporaryFile).

write(data): Writes data (str or bytes) to the file.

read(size): Reads size (int) bytes/characters of the file.

seek(offset): Goes to the byte position offset (int) in the file. E.g., await myfile.seek(0) would go to the start of the file.
This is especially useful if you run await myfile.read() once and then need to read the contents again.

close(): Closes the file.
As all these methods are async methods, you need to "await" them.

For example, inside of an async path operation function you can get the contents with:
contents = await myfile.read()

If you are inside of a normal def path operation function, you can access the UploadFile.file directly, for example:
contents = myfile.file.read()

FastAPI's UploadFile inherits directly from Starlette's UploadFile, but adds some necessary parts to
make it compatible with Pydantic and the other parts of FastAPI."""


"""What is "Form Data"¶
The way HTML forms (<form></form>) sends the data to the server normally uses a "special" encoding for that data,
it's different from JSON.

FastAPI will make sure to read that data from the right place instead of JSON.

Data from forms is normally encoded using the "media type" 'application/x-www-form-urlencoded' when it doesn't include files.

But when the form includes files, it is encoded as 'multipart/form-data'. If you use File, FastAPI will know
it has to get the files from the correct part of the body.

You can declare multiple File and Form parameters in a path operation, but you can't also declare Body fields
that you expect to receive as JSON, as the request will have the body encoded using multipart/form-data instead of application/json.

This is not a limitation of FastAPI, it's part of the HTTP protocol."""


"""Optional File Upload¶
You can make a file optional by using standard type annotations and setting a default value of None:"""

@app.post("/data/")
async def get_data(param_data: Annotated[bytes | None, File()] = None):
    if not param_data:
        return {"message" : "No file sent"}
    return {"File Size" : len(param_data)}

@app.post("/uploads/")
async def upload_data(param_uploads: UploadFile | None = None):
    if not upload_data:
        return {"message" : "No file sent"}
    return {"File Name" : param_uploads.filename}


"""UploadFile with Additional Metadata¶
You can also use File() with UploadFile, for example, to set additional metadata:"""

@app.post("/addition/")
async def get_add_data(add_data: Annotated[bytes, File(description="This is an additional information for File type")]):
    if not add_data:
        return {"message" : "No file sent"}
    return {"File Size" : len(add_data)}

async def get_upload_file(param_file: Annotated[UploadFile, File(description="Additional Info for UploadFile")]):
    if not param_file:
        return {"message" : "No file sent"}
    return {"File Name" : param_file.filename}

"""Multiple File Uploads¶
It's possible to upload several files at the same time.

They would be associated to the same "form field" sent using "form data".

To use that, declare a list of bytes or UploadFile:"""

@app.post("/multiples/")
async def get_multiples(param_multiples: Annotated[list[bytes], File()]):
    if not param_multiples:
        return {"message" : "No files sent"}
    return {"File Sizes" : [len(file) for file in param_multiples]}

async def get_multiple_file(multiple_file: list[UploadFile]):
    if not multiple_file:
        return {"message" : "No files sent"}
    return {"File Names" : [file.filename for file in multiple_file]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content) # Remember to import HTMLResponse from fastapi.responses


"""Multiple File Uploads with Additional Metadata¶
And the same way as before, you can use File() to set additional parameters, even for UploadFile:"""

@app.post("/multipledata/")
async def get_multiple_data(param_mul_data: Annotated[list[bytes], File(description="Multiple additional information")]):
    if not param_mul_data:
        return {"message" : "No files sent"}
    return {"Files Sizes" : [len(mul_file) for mul_file in param_mul_data]}

@app.post("/multipleuploads/")
async def get_multiple_uploads(param_multiple_uploads: Annotated[list[UploadFile],
                                                                 File(description="Multiple files with additional information")]):
    if not param_multiple_uploads:
        return {"message" : "No files sent"}
    return {"File Names" : [files.filename for files in param_multiple_uploads]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)