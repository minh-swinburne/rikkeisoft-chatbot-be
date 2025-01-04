from fastapi import APIRouter, UploadFile, HTTPException, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
from bs4 import BeautifulSoup
from pathlib import Path
from app.core.config import settings
import re
import json
import uuid
import datetime
import requests


router = APIRouter()


@router.get("/{doc_id}")
async def get_doc(doc_id: str):
    return {"doc_id": doc_id}


@router.post("/")
async def upload_doc(
    file: Optional[UploadFile] = File(None),
    link: Optional[str] = Form(None),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    categories: List[str] = Form(...),
    creator: Optional[str] = Form(None),
    created_date: Optional[datetime.date] = Form(None),
    restricted: bool = Form(...),
    uploader: str = Form(...),  # Admin ID / Model
):
    # Prepare directory and file path
    file_dir = settings.upload_dir
    file_dir.mkdir(exist_ok=True)

    if not file_dir.exists():
        raise HTTPException(status_code=500, detail="Upload directory does not exist.")

    if file:
        # Define supported MIME types
        supported_types = {
            "application/pdf": "pdf",
            "application/msword": "doc",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
            "application/vnd.ms-excel": "xls",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
        }

        # Check if the uploaded file type is supported
        if file.content_type not in supported_types:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.content_type}. Supported types are: {', '.join(supported_types.values())}",
            )

        filename = file.filename
        file_type = supported_types[file.content_type]
        file_path = file_dir / file.filename

        if file_path.exists():
            raise HTTPException(
                status_code=400,
                detail=f"File {file_path.resolve()} already exists.",
            )

        # Save the uploaded file
        with file_path.open("wb") as f:
            content = await file.read()
            f.write(content)

    elif link:
        # Crawl web link
        try:
            response = requests.get(link)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract page title and sanitize it for filename
            page_title = soup.title.string if soup.title else "web_content"
            sanitized_title = re.sub(r"[^\w\s-]", "", page_title).strip()
            sanitized_title = re.sub(r"[-\s]+", "_", sanitized_title)

            # Save crawled content as an .html file
            filename = f"{sanitized_title}.html"
            file_type = "web_content"
            file_path = file_dir / filename

            with file_path.open("w", encoding="utf-8") as f:
                f.write(soup.prettify())

        except requests.RequestException as e:
            raise HTTPException(
                status_code=400, detail=f"Error crawling web link: {str(e)}"
            )

    else:
        raise HTTPException(
            status_code=400, detail="Either a file or a link must be provided."
        )

    # Should be replaced with Pydantic model later
    metadata = {
        "id": str(uuid.uuid4()),
        "filename": filename,
        "file_type": file_type,
        "title": title,
        "description": description,
        "categories": categories,
        "creator": creator, # Should find user ID from username
        "created_date": created_date,
        "restricted": restricted,
        "uploader": uploader, # Should find user ID from username
        "uploaded_time": datetime.datetime.now().isoformat(),
    }

    # Save metadata as a JSON file (should be changed to DB later)
    metadata_path = file_path.with_suffix(".json")

    with metadata_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    return {
        "message": f"{"File" if file else "Link"} uploaded {"successfully" if file_path.exists() else "failed"}. Upload path: {file_path}",
        "metadata": metadata,
    }
