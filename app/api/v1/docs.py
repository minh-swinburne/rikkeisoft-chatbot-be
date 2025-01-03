from fastapi import APIRouter, UploadFile, HTTPException, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
from pathlib import Path
from app.core.config import settings

import uuid
import datetime


router = APIRouter()


@router.get("/{doc_id}")
async def get_doc(doc_id: str):
    return {"doc_id": doc_id}


@router.post("/")
async def upload_doc(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    categories: List[str] = Form(...),
    creator: Optional[str] = Form(None),
    restricted: bool = Form(...),
    uploader: str = Form(...),  # Admin ID / Model
):
    file_dir = Path(settings.upload_dir)
    file_dir.mkdir(exist_ok=True)

    file_path = file_dir / file.filename
    with file_path.open("wb") as f:
        content = await file.read()
        f.write(content)

    metadata = {
        "id": str(uuid.uuid4()),
        "filename": file.filename,
        "title": title,
        "description": description,
        "categories": categories,
        "creator": creator,
        "restricted": restricted,
        "uploader": uploader,
        "uploaded_time": datetime.datetime.now().isoformat(),
    }

    # Save metadata as a JSON file (should be changed to DB later)
    metadata_path = file_path.with_suffix(".json")
    metadata_path.write_text(str(metadata))

    return {
        "message": "File uploaded successfully",
        "metadata": metadata,
    }
