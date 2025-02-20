from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repos.category import CategoryRepository
from app.repos import _commit_and_refresh
from app.models import Document, DocumentStatus
from app.schemas import DocumentBase, DocumentUpdate, DocumentStatusModel
from datetime import datetime
from typing import Optional
import uuid


class DocumentRepository:
    @staticmethod
    async def create(db: AsyncSession, document_data: DocumentBase) -> Document:
        """
        Create a new document entry.
        """
        print(document_data.categories)
        categories = []
        for category_str in document_data.categories:
            if category_str == "":
                continue
            category = await CategoryRepository.get_by_name(db, category_str)
            if not category:
                raise ValueError(f"Category with name {category_str} not found.")
            categories.append(category)

        document_data.categories = categories
        document = Document(
            id=str(uuid.uuid4()),
            **document_data.model_dump(),
            uploaded_time=datetime.now(),
            last_modified=datetime.now(),
        )
        document.status = DocumentStatus(document_id=document.id)

        db.add(document)
        return await _commit_and_refresh(db, document)

    @staticmethod
    async def list_all(db: AsyncSession) -> list[Document]:
        """
        List all documents.
        """
        result = await db.execute(select(Document))
        return result.scalars().unique().all()
    
    @staticmethod
    async def list_by_creator(db: AsyncSession, creator: str) -> list[Document]:
        """
        List all documents by a specific creator.
        """
        result = await db.execute(select(Document).where(Document.creator == creator))
        return result.scalars().unique().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, document_id: str) -> Optional[Document]:
        """
        Get a document by its ID.
        """
        return await db.get(Document, document_id)

    @staticmethod
    async def update(
        db: AsyncSession, document_id: str, updates: DocumentUpdate
    ) -> Document:
        """
        Update an existing document.
        """
        document = await DocumentRepository.get_by_id(db, document_id)
        if not document:
            raise ValueError(f"Document with ID {document_id} not found.")
        for key, value in updates.model_dump(exclude_unset=True).items():
            if key == "status": # One-to-one relationship
                print("Status value:", value)
                for status_key, status_value in value.items():
                    setattr(document.status, status_key, status_value)
                continue
            if key == "categories": # One-to-many relationship
                categories = []
                for category_str in value:
                    category = await CategoryRepository.get_by_name(db, category_str)
                    if not category:
                        raise ValueError(f"Category with name {category_str} not found.")
                    categories.append(category)
                value = categories
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
