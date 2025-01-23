from sqlalchemy.ext.asyncio import AsyncSession
from app.repos.document import DocumentRepository
from app.core.config import settings
from app.schemas import DocumentBase, DocumentModel, DocumentUpdate, DocumentStatusModel
from app.models import Document
from .user import UserService
from bs4 import BeautifulSoup  # For .html
from docx import Document as Docx  # For .docx
from typing import Optional
from PIL import Image
import pytesseract
import openpyxl  # For .xlsx
import fitz  # PyMuPDF for PDF
import io


pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd


class DocumentService:
    """
    Handles business logic for document management, including text extraction, CRUD operations, and processing.
    """
    @staticmethod
    async def modelize_document(db: AsyncSession, document: Document) -> DocumentModel:
        """Create a new document in the database."""
        document.creator = await UserService.get_user_by_id(db, document.creator)
        document.uploader = await UserService.get_user_by_id(db, document.uploader)
        print(document.__dict__)
        return document

    @staticmethod
    async def create_document(
        db: AsyncSession, doc_data: DocumentBase
    ) -> DocumentModel:
        """Create a new document in the database."""
        document = await DocumentRepository.create(db, doc_data)
        document = await DocumentService.modelize_document(db, document)
        return DocumentModel.model_validate(document)

    @staticmethod
    async def list_documents(db: AsyncSession) -> list[DocumentModel]:
        """List all documents in the database."""
        docs = await DocumentRepository.list(db)
        print("Docs:", docs[0].__dict__)
        return [
            DocumentModel.model_validate(
                await DocumentService.modelize_document(db, doc)
            )
            for doc in docs
        ]

    @staticmethod
    async def get_document_by_id(
        db: AsyncSession, doc_id: str
    ) -> Optional[DocumentModel]:
        """Retrieve a document by its ID."""
        document = await DocumentRepository.get_by_id(db, doc_id)
        document = await DocumentService.modelize_document(db, document)
        return DocumentModel.model_validate(document) if document else None

    @staticmethod
    async def update_document(
        db: AsyncSession, doc_id: str, updates: DocumentUpdate
    ) -> Optional[DocumentModel]:
        """Update document details."""
        document = await DocumentRepository.update(db, doc_id, updates)
        document = await DocumentService.modelize_document(db, document)
        return DocumentModel.model_validate(document) if document else None

    @staticmethod
    async def update_status(
        db: AsyncSession, updates: DocumentStatusModel
    ) -> Optional[DocumentModel]:
        """Update document status."""
        status = await DocumentRepository.update_status(db, updates)
        return DocumentStatusModel.model_validate(status) if status else None

    @staticmethod
    async def delete_document(db: AsyncSession, doc_id: str) -> bool:
        """Delete a document by its ID."""
        from app.bot.vector_db import delete_data

        delete_data(doc_id)
        return await DocumentRepository.delete(db, doc_id)

    @staticmethod
    async def upload_document(file_content: bytes | str, filename: str) -> str:
        # Prepare directory and file path
        file_dir = settings.upload_dir
        file_dir.mkdir(exist_ok=True)
        file_path = file_dir / filename

        if not file_dir.exists():
            raise FileNotFoundError("Upload directory not found.")

        with open(file_path, "wb" if isinstance(file_content, bytes) else "w") as file:
            file.write(file_content)

        return file_path

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
        words = text.split()
        chunks = [
            " ".join(words[i : i + chunk_size])
            for i in range(0, len(words), chunk_size - overlap)
        ]
        return chunks

    @staticmethod
    def extract_text(file_path: str, file_type: str) -> str:
        """Extract text from a file based on its type."""
        extractors = {
            "pdf": DocumentService._extract_text_from_pdf,
            "docx": DocumentService._extract_text_from_doc,
            "xlsx": DocumentService._extract_text_from_excel,
            "html": DocumentService._extract_text_from_html,
        }
        if file_type not in extractors:
            raise ValueError(f"Unsupported file type: {file_type}")
        return extractors[file_type](file_path)

    @staticmethod
    async def embed_document(document: DocumentModel, file_path: str) -> bool:
        from app.bot.embedding import get_embedding
        from app.bot.vector_db import insert_data

        text = DocumentService.extract_text(file_path, document.file_type)
        chunks = DocumentService.chunk_text(text)
        embeddings = get_embedding(chunks)
        data = []

        for chunk, embedding in zip(chunks, embeddings):
            data.append(
                {
                    "document_id": document.id,
                    "title": document.title,
                    "text": chunk,
                    "embedding": embedding,
                    "meta": {
                        "description": document.description,
                        "categories": document.categories,
                        "creator": document.creator,
                        "created_date": document.created_date,
                        "restricted": document.restricted,
                        "uploader": document.uploader,
                        "uploaded_time": document.uploaded_time,
                        "url": document.url,
                        "last_modified": document.last_modified,
                    },
                }
            )

        insert_data(data)

    @staticmethod
    def _extract_text_from_pdf(file_path: str) -> str:
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                page_text = page.get_text()
                if not page_text.strip():
                    images = page.get_images(full=True)
                    for img_index, img in enumerate(images):
                        xref = img[0]
                        base_image = pdf.extract_image(xref)
                        image_bytes = base_image["image"]
                        image = Image.open(io.BytesIO(image_bytes))
                        ocr_text = pytesseract.image_to_string(image)
                        text += f"OCR - Page {page.number}, Image {img_index + 1}:\n{ocr_text}\n"
                else:
                    text += page_text
        return text

    @staticmethod
    def _extract_text_from_doc(file_path: str) -> str:
        doc = Docx(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    @staticmethod
    def _extract_text_from_excel(file_path: str) -> str:
        text = ""
        workbook = openpyxl.load_workbook(file_path)
        for sheet in workbook.worksheets:
            for row in sheet.iter_rows(values_only=True):
                text += " ".join(map(str, row)) + "\n"
        return text

    @staticmethod
    def _extract_text_from_html(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            return soup.get_text()
