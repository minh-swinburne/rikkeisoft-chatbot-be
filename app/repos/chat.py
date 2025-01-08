# Just temporary, will be replaced in the future when we have a database
import json
import uuid
from datetime import datetime


class ChatRepository:
    def __init__(self):
        self._storage: dict[str, dict] = {}
        self.load()


    def load(self):
        with open("app/data/chats.json", "r") as f:
            chats = json.load(f)

        with open("app/data/messages.json", "r") as f:
            messages = json.load(f)

        for chat in chats:
            chat_id = chat["id"]
            self._storage[chat_id] = {
                **chat,
                "messages": {},
            }

        for message in messages:
            chat_id = message["chat_id"]
            self._storage[chat_id]["messages"][message["id"]] = message


    def save(self):
        chats = list(self._storage.values())
        with open("app/data/chats.json", "w") as f:
            json.dump(chats, f, indent=4)

        messages = []
        for chat in self._storage.values():
            messages.extend(chat["messages"])

        with open("app/data/messages.json", "w") as f:
            json.dump(messages, f, indent=4)


    def create_chat(self, chat: dict) -> dict:
        chat_id = str(uuid.uuid4())

        chat["id"] = chat_id
        chat["messages"] = {}
        chat["last_access"] = datetime.now()

        self._storage[chat_id] = chat
        return chat


    def create_message(self, message: dict) -> dict:
        chat_id = message["chat_id"]
        if chat_id not in self._storage:
            raise ValueError(f"Chat {chat_id} does not exist")

        message_id = str(uuid.uuid4())
        message["id"] = message_id

        self._storage[chat_id]["messages"][message_id] = message
        self._storage[chat_id]["last_access"] = message["time"]

        # if len(self._storage[chat_id]["messages"]) == 1:
        #     self._storage[chat_id]["created_date"] = message["time"]

        return message


    def get_chat(self, chat_id: str) -> dict:
        return self._storage.get(chat_id)


    def get_message(self, chat_id: str, message_id: str) -> dict:
        return self._storage.get(chat_id)["messages"].get(message_id)


    def list_chats(self) -> list[dict]:
        return list(self._storage.values())


    def list_messages(self, chat_id: str) -> list[dict]:
        if chat_id not in self._storage:
            raise ValueError(f"Chat {chat_id} does not exist")
        return list(self._storage.get(chat_id).get("messages").values())


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
