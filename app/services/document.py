from sqlalchemy.ext.asyncio import AsyncSession
from app.repos.document import DocumentRepository
from app.core.config import settings
from app.schemas.docs import *
from app.bot.rag import process_document
from datetime import datetime
from bs4 import BeautifulSoup  # For .html
from pathlib import Path
from docx import Document  # For .docx
from PIL import Image
import pytesseract
import subprocess
import requests
import openpyxl  # For .xlsx
import fitz  # PyMuPDF for PDF
import uuid
import io
import re


pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd


class DocumentService:
    """
    Handles business logic for document management, including text extraction, CRUD operations, and processing.
    """

    def __init__(self, repository: DocumentRepository):
        self.repository = repository

    async def create_document(
        self, db: AsyncSession, doc_data: DocumentBase
    ) -> DocumentModel:
        """Create a new document in the database."""
        doc = await self.repository.create(db, doc_data)
        return DocumentModel.model_validate(doc)

    async def get_document_by_id(
        self, db: AsyncSession, doc_id: str
    ) -> Optional[DocumentModel]:
        """Retrieve a document by its ID."""
        doc = await self.repository.get_by_id(db, doc_id)
        return DocumentModel.model_validate(doc) if doc else None

    async def update_document(
        self, db: AsyncSession, doc_id: str, updates: DocumentUpdate
    ) -> Optional[DocumentModel]:
        """Update document details."""
        doc = await self.repository.update(db, doc_id, updates)
        return DocumentModel.model_validate(doc) if doc else None

    async def delete_document(self, db: AsyncSession, doc_id: str) -> bool:
        """Delete a document by its ID."""
        return await self.repository.delete(db, doc_id)

    async def upload_document(
        self, db: AsyncSession, file_content: bytes | str, doc_data: DocumentBase
    ) -> DocumentModel:
        # Prepare directory and file path
        file_dir = settings.upload_dir
        file_dir.mkdir(exist_ok=True)

        if not file_dir.exists():
            raise FileNotFoundError("Upload directory not found.")

        file_path = file_dir / doc_data.filename
        with open(file_path, "wb" if isinstance(file_content, bytes) else "w") as file:
            file.write(file_content)

        document = await self.create_document(db, doc_data)
        categories = list(map(lambda category: category.name, document.categories))

        # Should be done in a background task
        await process_document(
            file_path,
            document.file_type,
            {   # Document metadata
                "document_id": document.id,
                "title": document.title,
                "description": document.description,
                "categories": categories,
                "creator": document.creator,
                "created_date": document.created_date,
                "restricted": document.restricted,
                "uploader": document.uploader,
            },
        )

        return document

    def extract_text(self, file_path: str, file_type: str) -> str:
        """Extract text from a file based on its type."""
        extractors = {
            "pdf": self._extract_text_from_pdf,
            "docx": self._extract_text_from_doc,
            "xlsx": self._extract_text_from_excel,
            "html": self._extract_text_from_html,
        }
        if file_type not in extractors:
            raise ValueError(f"Unsupported file type: {file_type}")
        return extractors[file_type](file_path)

    def _extract_text_from_pdf(self, file_path: str) -> str:
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

    def _extract_text_from_doc(self, file_path: str) -> str:
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    def _extract_text_from_excel(self, file_path: str) -> str:
        text = ""
        workbook = openpyxl.load_workbook(file_path)
        for sheet in workbook.worksheets:
            for row in sheet.iter_rows(values_only=True):
                text += " ".join(map(str, row)) + "\n"
        return text

    def _extract_text_from_html(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            return soup.get_text()
