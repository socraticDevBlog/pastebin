import base64, hashlib, time
from typing import Dict

from dynamodb import DB


class Paste:
    """
    Paste

    Abstracts a Paste (an Item saved into the Pastebin)

    **can save itself via injected database object**

    """

    def __init__(self, content: str | bytes, db=None):
        if isinstance(content, str):
            b = base64.b64encode(bytes(content, "utf-8"))
        else:
            b = content
        if db is None:
            self._db = DB()
        else:
            self._db = db
        self._content = b.decode("utf-8")
        self._id = hashlib.sha1(content.encode("utf-8")).hexdigest()[:5]
        self._unix_timestamp = int(time.time())

    def dict(self) -> Dict:
        return {
            "id": self._id,
            "content": self._content,
            "created_timestamp": self._unix_timestamp,
        }

    def create(self):
        self._db.create(self.dict())


class PastebinClient:
    """
    PastebinClient

    high-level object that can interact with database

    and perform 'business' operations as requested by a user
    or a API call

    """

    def __init__(self, db=None):
        if db is None:
            self._db = DB()
        else:
            self._db = db

    def get_item(self, id: str) -> str:
        item = self._db.get_item(id=id)
        return item["Item"]

    def get_content(self, id: str) -> str:
        item = self.get_item(id=id)
        return item["Item"]["doc"]["content"]
