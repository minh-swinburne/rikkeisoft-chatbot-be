from typing import Optional
from app.schemas.document import Document
import uuid


class DocumentRepository:
    def __init__(self):
        self._storage: dict[str, dict] = {}

    def create(self, document: dict) -> str:
        document_id = str(uuid.uuid4())
        document["id"] = document_id
        self._storage[document_id] = document
        return document_id

    def get(self, doc_id: str) -> Optional[dict]:
        return self._storage.get(doc_id)

    def list(self) -> list[dict]:
        return list(self._storage.values())

    def update(self, document_id: str, updates: dict) -> bool:
        document = self.get(document_id)
        if not document:
            return False
        document.update(updates)
        return True

    def delete(self, document_id: str) -> bool:
        if document_id in self._storage:
            del self._storage[document_id]
            return True
        return False
