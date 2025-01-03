from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
import datetime

# Initialize the FastAPI application
app = FastAPI()

# Define the directory to store uploaded files
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)  # Ensure the upload directory exists

# Pydantic model to define the structure of document metadata
class DocumentMetadata(BaseModel):
    title: str  # Title of the document
    description: Optional[str] = None  # Optional description of the document
    categories: List[str]  # List of categories the document belongs to
    creator: Optional[str] = None  # Optional name of the document's creator
    restricted: bool  # Whether the document is restricted to admins only

# Define the endpoint for uploading documents
@app.post("/upload/")
async def upload_document(
    file: UploadFile = File(...),  # Uploaded file
    title: str = Form(...),  # Document title (form input)
    description: Optional[str] = Form(None),  # Optional description (form input)
    categories: List[str] = Form(...),  # Categories (form input, can accept multiple values)
    creator: Optional[str] = Form(None),  # Optional creator name (form input)
    restricted: bool = Form(...)  # Restriction flag (form input, true or false)
):
    # Save the uploaded file to the specified directory
    file_location = UPLOAD_DIR / file.filename  # Create a file path in the uploads directory
    with file_location.open("wb") as f:
        content = await file.read()  # Read the file content asynchronously
        f.write(content)  # Write the content to the file

    # Generate metadata for the uploaded file
    metadata = {
        "title": title,  # Document title
        "description": description,  # Document description
        "categories": categories,  # Document categories
        "creator": creator,  # Document creator
        "restricted": restricted,  # Whether the document is restricted
        "uploaded_time": datetime.datetime.now().isoformat(),  # Current timestamp
        "uploader": "Admin User"  # Placeholder for uploader (should be dynamically set in production)
    }

    # Save metadata as a JSON file (optional; could also save to a database)
    metadata_location = file_location.with_suffix(".json")  # Save metadata with .json extension
    metadata_location.write_text(str(metadata))  # Write metadata to the JSON file

    # Return a JSON response with a success message and metadata
    return JSONResponse(
        content={"message": "File uploaded successfully", "metadata": metadata},
        status_code=200,
    )

# Define a basic root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Document Upload API!"}
