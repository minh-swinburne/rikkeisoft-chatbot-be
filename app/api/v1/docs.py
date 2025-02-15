from fastapi import (
    APIRouter,
    HTTPException,
    status,
    UploadFile,
    WebSocket,
    Depends,
    Path,
    Body,
    Form,
    File,
)
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import validate_access_token
from app.core.database import get_db
from app.core.settings import settings
from app.services import DocumentService, UserService
from app.schemas import (
    DocumentBase,
    DocumentModel,
    DocumentUpdate,
    DocumentStatusBase,
    TokenModel,
)
from app.utils import get_file_type
from datetime import date
from bs4 import BeautifulSoup
from typing import Optional
import requests
import re


router = APIRouter()
authorized_roles = ["admin"]


@router.get("")
async def list_documents(
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> list[DocumentModel]:
    """
    List all documents. Users without the required roles will not see restricted documents.
    """
    documents = await DocumentService.list_documents(db)

    if not any(role in authorized_roles for role in token_payload.roles):
        documents = [doc for doc in documents if not doc.restricted]

    return [
        doc.model_dump(
            exclude={
                "creator_user": {"password", "username_last_changed"},
                "uploader_user": {"password", "username_last_changed"},
            },
            exclude_unset=True,
        )
        for doc in documents
    ]


@router.post("")
async def upload_document(
    file: Optional[UploadFile] = File(None),
    link: Optional[str] = Form(None),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    categories: list[str] = Form([]),
    creator: str = Form(),
    created_date: Optional[date] = Form(None),
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
        try:
            file_type = get_file_type(file.content_type)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting file type: {e}")

        file_name = file.filename
        file_size = file.size
        file_content = await file.read()

    elif link:
        # Crawl web link
        try:
            response = requests.get(link)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract page title and sanitize it for file_name
            page_title = soup.title.string if soup.title else title
            page_title = re.sub(r"[^\w\s-]", "", page_title).strip()
            # page_title = re.sub(r"[-\s]+", "_", page_title)

            # Save crawled content as an .html file
            file_name = f"{page_title}.html"
            file_type = "html"
            file_content = soup.prettify().encode("utf-8")
            file_size = len(file_content)

        except requests.RequestException as e:
            raise HTTPException(
                status_code=400, detail=f"Error crawling web link: {str(e)}"
            )
    else:
        raise HTTPException(
            status_code=400, detail="Either a file or a link must be provided."
        )

    if file_size > settings.upload_max_size * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the maximum limit of {settings.upload_max_size} MB.",
        )

    creator_user = await UserService.get_user_by_email(db, creator)

    if not creator_user:
        raise HTTPException(
            status_code=404, detail=f"User with ID '{creator}' not found."
        )

    print("Uploading file:")
    print("File name:", file_name)
    print("File type:", file_type)
    print("File size:", file_size, f"({file_size/1024/1024:.2f} MB)")
    if link:
        print("Link:", link)
    print("Title:", title)
    print("Description:", description)
    print("Categories:", categories)
    print("Creator:", creator_user.id, creator_user.email)
    print("Created date:", created_date)
    print("Restricted:", restricted)
    print("Uploader:", token_payload.sub, token_payload.email)

    document_data = DocumentBase(
        file_name=file_name,
        file_type=file_type,
        link_url=link if link else None,
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
        print("Uploading document to S3...")
        await DocumentService.update_document(
            db,
            document.id,
            DocumentUpdate(status=DocumentStatusBase(uploaded="processing")),
        )
        print("Document status updated to 'processing'")
        await DocumentService.upload_document(document, file_content)
        await DocumentService.update_document(
            db,
            document.id,
            DocumentUpdate(status=DocumentStatusBase(uploaded="complete")),
        )
        print("✅ Document uploaded successfully!")
    except Exception as e:
        print("❌ Error uploading document to S3:", e)
        await DocumentService.update_document(
            db,
            document.id,
            DocumentUpdate(status=DocumentStatusBase(uploaded="error")),
        )
        raise

    try:
        print("Embedding document...")
        await DocumentService.update_document(
            db,
            document.id,
            DocumentUpdate(status=DocumentStatusBase(embedded="processing")),
        )
        await DocumentService.embed_document(document, file_content)
        await DocumentService.update_document(
            db,
            document.id,
            DocumentUpdate(status=DocumentStatusBase(embedded="complete")),
        )
        print("✅ Document embedded successfully!")
    except Exception as e:
        print("❌ Error embedding document:", e)
        await DocumentService.update_document(
            db,
            document.id,
            DocumentUpdate(status=DocumentStatusBase(embedded="error")),
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
    print(updates)

    document = await DocumentService.update_document(db, doc_id, updates)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )
    return document


@router.delete("/{doc_id}", response_class=JSONResponse)
async def delete_document(
    doc_id: str = Path(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    if not any(role in authorized_roles for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Only admins can delete documents.",
        )

    result = await DocumentService.delete_document(db, doc_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )
    return JSONResponse(
        content={"success": result, "message": "Document deleted successfully"}
    )


@router.get("/{doc_id}/download")
async def download_document(
    doc_id: str = Path(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
):
    print("Download document")

    url = await DocumentService.generate_document_url(db, doc_id)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    print("Download URL:", url)
    return JSONResponse(content={"url": url})


@router.get("/{doc_id}/preview")
async def preview_document(
    doc_id: str = Path(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
):
    print("Preview document")

    url = await DocumentService.generate_document_url(db, doc_id, preview=True)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )
    print("Preview URL:", url)
    return JSONResponse(content={"url": url})
