import base64
import hashlib
import time
from typing import Dict


class Paste:
    """
    Paste

    Abstracts a Paste

    """

    def __init__(self, content: str = None, id: str = None, timestamp: int = None):
        if content is not None:
            b = base64.b64encode(bytes(content, "utf-8"))
            self._content = b.decode("utf-8")
        else:
            # will be removed by the time we go to prod
            self._content = "Im an empty paste obviously"
        if id is None:
            self._id = hashlib.sha1(self._content.encode("utf-8")).hexdigest()
        else:
            self._id = id
        if timestamp is None:
            self._unix_timestamp = int(time.time())
        else:
            self._unix_timestamp = timestamp

    def dict(self) -> Dict:
        return {
            "id": self._id,
            "content": self._content,
            "created_timestamp": self._unix_timestamp,
        }

    def to_string(self) -> str:
        return self._content
