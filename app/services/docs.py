from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.docs import Document
import uuid


# Create a new document entry
async def create_document(
    db: AsyncSession,
    filename: str,
    file_type: str,
    title: str,
    description: str,
    categories: list[str],
    creator: str,
    created_date,
    restricted: bool,
    uploader: str,
):
    doc = Document(
        id=str(uuid.uuid4()),
        filename=filename,
        file_type=file_type,
        title=title,
        description=description,
        categories=",".join(categories),  # Convert list to a comma-separated string
        creator=creator,
        created_date=created_date,
        restricted=restricted,
        uploader=uploader,
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc


# Retrieve a document by ID
async def get_document_by_id(db: AsyncSession, doc_id: str):
    result = await db.execute(select(Document).where(Document.id == doc_id))
    return result.scalar_one_or_none()
