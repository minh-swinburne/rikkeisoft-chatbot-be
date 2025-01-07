from typing import Optional
import uuid

class DocumentRepository:
    def __init__(self):
        self._storage: dict[str, dict] = {}

    def get(self, doc_id: str) -> dict:
        return self._storage.get(doc_id)

    def create(
        self,
        title: str,
        description: Optional[str],
        categories: list[str],
        creator: Optional[str],
        created_date: Optional[str],
        restricted: bool,
        uploader: str,
    ) -> str:
        doc_id = str(uuid.uuid4())
        doc = {
            "doc_id": doc_id,
            "title": title,
            "description": description,
            "categories": categories,
            "creator": creator,
            "created_date": created_date,
            "restricted": restricted,
            "uploader": uploader,
        }
        self._storage[doc_id] = doc
        return doc_id