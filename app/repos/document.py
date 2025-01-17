from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.documents import Document
from app.schemas.documents import DocumentBase, DocumentUpdate
from app.repos import _commit_and_refresh
from datetime import datetime
import uuid


class DocumentRepository:
    @staticmethod
    async def create(db: AsyncSession, document_data: DocumentBase) -> Document:
        """
        Create a new document entry.
        """
        document = Document(
            id=str(uuid.uuid4()),
            **document_data.model_dump(),
            uploaded_time=datetime.now(),
            last_modified=datetime.now(),
        )
        db.add(document)
        return await _commit_and_refresh(db, document)

    @staticmethod
    async def list(db: AsyncSession) -> list[Document]:
        """
        List all documents.
        """
        result = await db.execute(select(Document))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, document_id: str) -> Document | None:
        """
        Get a document by its ID.
        """
        return await db.get(Document, document_id)

    @staticmethod
    async def update(
        db: AsyncSession, document_id: str, update_data: DocumentUpdate
    ) -> Document | None:
        """
        Update an existing document.
        """
        document = await DocumentRepository.get_by_id(db, document_id)
        if not document:
            raise ValueError(f"Document with ID {document_id} not found.")
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(document, key, value)
        return await _commit_and_refresh(db, document)

    @staticmethod
    async def delete(db: AsyncSession, document_id: str) -> bool:
        """
        Delete a document by its ID.
        """
        document = await DocumentRepository.get_by_id(db, document_id)
        if not document:
            return False
        try:
            await db.delete(document)
            await db.commit()
        except:
            await db.rollback()
            raise
        return True
