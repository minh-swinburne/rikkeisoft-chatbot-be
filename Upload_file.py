from fastapi import FastAPI, File, Form, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
import datetime

# Initialize the FastAPI application
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the directory to store uploaded files
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)  # Ensure the upload directory exists

# Pydantic model for metadata
class DocumentMetadata(BaseModel):
    title: str
    description: Optional[str] = None
    categories: List[str]
    creator: Optional[str] = None
    restricted: bool

@app.post("/upload/")
async def upload_document(
    uploadType: str = Form(...),
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    categories: List[str] = Form(...),
    creator: Optional[str] = Form(None),
    restricted: bool = Form(...),
):
    if uploadType == "file":
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Save the file
        file_location = UPLOAD_DIR / file.filename
        with file_location.open("wb") as f:
            content = await file.read()
            f.write(content)

        # Metadata for the file
        metadata = {
            "type": "file",
            "title": title,
            "description": description,
            "categories": categories,
            "creator": creator,
            "restricted": restricted,
            "uploaded_time": datetime.datetime.now().isoformat(),
        }
    elif uploadType == "link":
        if not url:
            raise HTTPException(status_code=400, detail="No URL provided")

        # Metadata for the web link
        metadata = {
            "type": "link",
            "url": url,
            "title": title,
            "description": description,
            "categories": categories,
            "creator": creator,
            "restricted": restricted,
            "uploaded_time": datetime.datetime.now().isoformat(),
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid upload type")

    # Save metadata (optional, can use a database instead)
    metadata_location = UPLOAD_DIR / f"{title.replace(' ', '_')}_metadata.json"
    metadata_location.write_text(str(metadata))

    return JSONResponse(
        content={"message": f"{uploadType.capitalize()} uploaded successfully", "metadata": metadata},
        status_code=200,
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the Document Upload API!"}
