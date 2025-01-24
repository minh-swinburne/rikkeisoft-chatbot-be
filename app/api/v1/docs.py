from fastapi import (
    APIRouter,
    HTTPException,
    status,
    UploadFile,
    Depends,
    Path,
    Body,
    Form,
    File,
)
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import validate_access_token
from app.core.database import get_db
from app.core.config import settings
from app.services import DocumentService, UserService
from app.schemas import (
    DocumentBase,
    DocumentModel,
    DocumentUpdate,
    DocumentStatusModel,
    TokenModel,
)
from datetime import date, datetime
from bs4 import BeautifulSoup
from typing import Optional
import subprocess
import requests
import asyncio
import re


router = APIRouter()
authorized_roles = ["admin"]


@router.get("")
async def list_documents(
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> list[DocumentModel]:
    """
    List all documents.
    """
    if not any(role in authorized_roles for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Only admins can access the documents.",
        )

    documents = await DocumentService.list_documents(db)
    return documents


@router.post("")
async def upload_document(
    file: Optional[UploadFile] = File(None),
    link: Optional[str] = Form(None),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    categories: list[str] = Form([]),
    creator: str = Form(),
    created_date: Optional[date] = Form(None, alias="createdDate"),
    restricted: bool = Form(False),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> DocumentModel:
    """
    Create a new document.
    """
    if not any(role in authorized_roles for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Only admins can create documents.",
        )

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
        file_content = await file.read()

    elif link:
        # Crawl web link
        try:
            response = requests.get(link)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract page title and sanitize it for filename
            page_title = soup.title.string if soup.title else title
            sanitized_title = re.sub(r"[^\w\s-]", "", page_title).strip()
            sanitized_title = re.sub(r"[-\s]+", "_", sanitized_title)

            # Save crawled content as an .html file
            filename = f"{sanitized_title}.html"
            file_type = "html"
            file_content = soup.prettify()

        except requests.RequestException as e:
            raise HTTPException(
                status_code=400, detail=f"Error crawling web link: {str(e)}"
            )

    else:
        raise HTTPException(
            status_code=400, detail="Either a file or a link must be provided."
        )

    creator_user = await UserService.get_user_by_email(db, creator)

    if not creator_user:
        raise HTTPException(
            status_code=404, detail=f"User with ID '{creator}' not found."
        )

    print("Creator:", creator_user)
    print("Creator ID:", creator_user.id)

    document_data = DocumentBase(
        filename=filename,
        file_type=file_type,
        url=link if link else None,
        title=title,
        description=description,
        categories=categories,
        creator=creator_user.id,
        created_date=created_date,
        restricted=restricted,
        uploader=token_payload.sub,
    )

    document = await DocumentService.create_document(db, document_data)

    # Should be done in the background
    try:
        DocumentService.update_status(
            db,
            DocumentStatusModel(
                document_id=document.id, uploaded="processing", embedded="pending"
            ),
        )
        file_path = await DocumentService.upload_document(
            file_content, document.filename
        )
        DocumentService.update_status(
            db,
            DocumentStatusModel(
                document_id=document.id, uploaded="complete", embedded="pending"
            ),
        )
    except:
        DocumentService.update_status(
            db,
            DocumentStatusModel(
                document_id=document.id, uploaded="error", embedded="pending"
            ),
        )
        raise

    try:
        DocumentService.update_status(
            db,
            DocumentStatusModel(
                document_id=document.id, uploaded="complete", embedded="processing"
            ),
        )
        await DocumentService.embed_document(document, file_path)
        DocumentService.update_status(
            db,
            DocumentStatusModel(
                document_id=document.id, uploaded="complete", embedded="complete"
            ),
        )
    except:
        DocumentService.update_status(
            db,
            DocumentStatusModel(
                document_id=document.id, uploaded="complete", embedded="error"
            ),
        )
        raise

    return document


@router.get("/{doc_id}")
async def get_document(
    doc_id: str = Path(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
):
    if not any(role in authorized_roles for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Only admins can access the documents.",
        )

    document = await DocumentService.get_document_by_id(db, doc_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.put("/{doc_id}")
async def edit_document(
    doc_id: str = Path(...),
    updates: DocumentUpdate = Body(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
):
    if not any(role in authorized_roles for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Only admins can update documents.",
        )

    document = await DocumentService.update_document(db, doc_id, updates)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{doc_id}")
async def delete_document(
    doc_id: str = Path(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
):
    if not any(role in authorized_roles for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Only admins can delete documents.",
        )

    result = await DocumentService.delete_document(db, doc_id)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    return JSONResponse(content={"message": "Document deleted successfully"})


# @router.get("/{doc_id}/download")
# async def download_document(
#     doc_id: str = Path(...),
#     token_payload: TokenModel = Depends(validate_access_token),
#     db: AsyncSession = Depends(get_db),
# ):
#     print("Download document")
#     if not any(role in authorized_roles for role in token_payload.roles):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Insufficient permissions. Only admins can download documents.",
#         )

#     document = await DocumentService.get_document_by_id(db, doc_id)
#     if not document:
#         raise HTTPException(status_code=404, detail="Document not found")

#     file_dir = settings.upload_dir
#     file_path = file_dir / document.filename

#     if not file_path.exists():
#         raise HTTPException(status_code=404, detail="Document file not found")

#     return FileResponse(
#         file_path, filename=document.filename, media_type="application/octet-stream"
#     )


@router.get("/{doc_id}/preview")
async def preview_document(
    doc_id: str = Path(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
):
    print("Preview document")
    if not any(role in authorized_roles for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Only admins can preview documents.",
        )

    document = await DocumentService.get_document_by_id(db, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.file_type == "html":
        return document.url

    file_dir = settings.upload_dir
    file_path = file_dir / document.filename

    if not file_path.exists():
        print(file_path)
        raise HTTPException(status_code=404, detail="Document file not found")

    url = settings.doc_preview_url + "http://ieee802.org/secmail/docIZSEwEqHFr.doc"
    # url = settings.doc_preview_url + file_path.name

    print("Preview URL:", url)

    return url
