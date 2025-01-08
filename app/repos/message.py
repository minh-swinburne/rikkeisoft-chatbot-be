# Just temporary, will be removed in the future when we have a database

import uuid

class MessageRepository:
    def __init__(self):
        self._storage: dict[str, dict] = {}

    def create(self, message: dict) -> str:
        message_id = str(uuid.uuid4())
        message["id"] = message_id
        self._storage[message_id] = message
        return message_id

    def get(self, message_id: str) -> dict:
        return self._storage.get(message_id)

    def list(self) -> list[dict]:
        return list(self._storage.values())

    def update(self, message_id: str, updates: dict) -> bool:
        message = self.get(message_id)
        if not message:
            return False
        message.update(updates)
        return True

    def delete(self, message_id: str) -> bool:
        if message_id in self._storage:
            del self._storage[message_id]
            return True
        return False