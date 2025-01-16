from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Form
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from bs4 import BeautifulSoup
from pathlib import Path
from app.schemas.docs import Document
from app.models.docs import DocumentBase
from app.services.docs import (
    create_document,
    get_document_by_id,
    update_document,
    delete_document,
)
from app.services.users import get_user_by_email
from app.bot.rag import process_document
from app.core.database import get_db
from app.core.config import settings
from app.utils import executor
import re
import json
import uuid
import datetime
import requests
import subprocess
import os



router = APIRouter()

@router.get("/{doc_id}/download")
async def download_file(doc_id: str, db: AsyncSession = Depends(get_db)):
    document = await get_document_by_id(db, doc_id)
    filename = document.filename
    file_path = os.path.join("uploads", filename)  # Assuming your files are named with their IDs
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)

@router.get("/{doc_id}/preview")
async def get_pdf(doc_id: str, db: AsyncSession = Depends(get_db)):
    document = await get_document_by_id(db, doc_id)
    filename = document.filename
    print("File name: ", filename)
    file_path = os.path.join("uploads", filename)   
    print("File path: ", file_path) 
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    file_extension = filename.split('.')[-1].lower()

    # If the file is already a PDF, serve it directly
    if file_extension == "pdf":
        return FileResponse(file_path, media_type="application/pdf")

    # If the file is DOCX, convert it to PDF using LibreOffice
    if file_extension == "docx":
        pdf_filename = filename.replace(".docx", ".pdf")
        pdf_path = os.path.join("files", pdf_filename)
        
        # Convert DOCX to PDF using LibreOffice (headless)
        subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", file_path], check=True)
        
        return FileResponse(pdf_path, media_type="application/pdf")

    # If the file is XLSX, convert it to PDF using LibreOffice
    if file_extension == "xlsx":
        pdf_filename = filename.replace(".xlsx", ".pdf")
        pdf_path = os.path.join("files", pdf_filename)
        
        # Convert XLSX to PDF using LibreOffice (headless)
        subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", file_path], check=True)
        
        return FileResponse(pdf_path, media_type="application/pdf")

    # If the file type is not supported, return an error
    raise HTTPException(status_code=415, detail="Unsupported file type")


@router.get("/")
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DocumentBase))
    return result.scalars().all()

@router.put("/{doc_id}/edit")
async def update_document_details(
    doc_id: str,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    categories: Optional[List[str]] = Form(None),
    restricted: Optional[bool] = Form(None),
    db: AsyncSession = Depends(get_db),
):
    print("Data recieved: ", doc_id, " ",title, " ",description, " ",categories, " ",restricted)
    try:

        document = await update_document(db, doc_id, title, description, categories, restricted)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.delete("/{doc_id}/delete")
async def delete_document_entry(doc_id: str, db: AsyncSession = Depends(get_db)):
    result = await delete_document(db, doc_id)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    return JSONResponse(content={"message": "Document deleted successfully"})


@router.get("/{doc_id}")
async def get_document(doc_id: str, db: AsyncSession = Depends(get_db)):
    document = await get_document_by_id(db, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.post("/")
async def upload_document(
    file: Optional[UploadFile] = File(None),
    link: Optional[str] = Form(None),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    categories: list[str] = Form(...),
    creator: Optional[str] = Form(None),
    created_date: Optional[datetime.date] = Form(None, alias="createdDate"),
    restricted: bool = Form(...),
    uploader: str = Form(...),  # Admin ID / Model
    db: AsyncSession = Depends(get_db),
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
            # "application/msword": "doc",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
            # "application/vnd.ms-excel": "xls",
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

    creator_user = await get_user_by_email(db, creator)
    uploader_user = await get_user_by_email(db, uploader)

    # Create the document entry in the database
    document = await create_document(
        db=db,
        filename=filename,
        file_type=file_type,
        title=title,
        description=description,
        categories=categories,
        creator=creator_user.id,
        created_date=created_date,
        restricted=restricted,
        uploader=uploader_user.id,
    )

    # subprocess.Popen(["python", "app/bot/rag.py", file_path, file_type, json.dumps(document.__dict__)])
    await process_document(file_path, file_type, {
        "document_id": document.id,
        "title": title,
        "description": description,
        "categories": categories,
        "creator": creator_user.id,
        "created_date": created_date,
        "restricted": restricted,
        "uploader": uploader_user.id,
        "uploaded_time": document.uploaded_time
    })

    return {"message": "Upload successful", "document": document}
