import base64
from typing import Dict

from dynamodb import DB
from paste import Paste


class PasteDataAware(Paste):
    """
    PasteDataAware

    Extension Paste class with database awareness
    """

    def __init__(self, content: str | bytes, id: str = None, db=None):
        if db is None:
            self._db = DB()
        else:
            self._db = db

        super().__init__(id=id, content=content)

    def create(self) -> str:
        return self._db.create(self.dict())


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

    def get_paste(self, id: str) -> Paste:
        item = self.get_item(id=id)
        id = item["Item"]["doc"]["id"]
        content_base64 = item["Item"]["doc"]["content"]
        content = base64.b64decode(content_base64)
        return Paste(id=id, content=content)
