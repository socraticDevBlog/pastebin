import base64
import hashlib
import time
from typing import Dict

DEFAULT_ENCODING = "utf-8"


class Paste:
    """
    Paste

    Abstracts a Paste

    basic Paste operations are implemented

    - create a Unique Identifier for a new Paste
    - Base64 encode for a new Paste
    - Base64 decode an existing Paste content into a human-readable string

    Public functions

    - Dict(): returns Paste infos in a dictionary format

    """

    def __init__(self, content: str = None, id: str = None, timestamp: int = None):
        if content is not None:
            self._base_64_content = self._base64_encode_str(content=content)
        else:
            self._base_64_content = ""
        if id is None:
            self.id = hashlib.sha1(
                self._base_64_content.encode(DEFAULT_ENCODING)
            ).hexdigest()
        else:
            self.id = id
        if timestamp is None:
            self._unix_timestamp = int(time.time())
        else:
            self._unix_timestamp = timestamp

    def dict(self) -> Dict:
        return {
            "id": self._id,
            "content": self._base64_decode_content(),
            "isBase64Encoded": False,
            "encoding": DEFAULT_ENCODING,
            "created_time_epoch": self._unix_timestamp,
        }

    def _base64_decode_content(self, encoding: str = DEFAULT_ENCODING) -> str:
        base64_content_bytes = self._base_64_content.encode(encoding=encoding)
        content_bytes = base64.b64decode(base64_content_bytes)
        return content_bytes.decode(encoding=encoding)

    def _base64_encode_str(self, content: str, encoding: str = DEFAULT_ENCODING) -> str:
        b = base64.b64encode(bytes(content, encoding))
        return b.decode(encoding)
