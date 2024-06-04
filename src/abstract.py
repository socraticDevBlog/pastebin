import base64
import hashlib
import time
from typing import Dict

DEFAULT_ENCODING = "utf-8"

KEY_CLIENT_ID = "client_identifier"


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

    def __init__(
        self,
        ttl: int,
        content: str = None,
        id: str = None,
        timestamp: int = None,
        client_identifier: str = None,
    ):
        if content is None:
            self._base_64_content = ""
        elif not self.is_base64_encoded(content=content):
            self._base_64_content = self._base64_encode_str(content=content)
        else:
            self._base_64_content = content
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

        self._metadata = {}

        if client_identifier is not None:
            self._metadata[KEY_CLIENT_ID] = client_identifier

        if ttl is not None:
            self._ttl_timestamp = int(time.time()) + ttl

    def dict(self) -> Dict:

        return {
            "id": self.id,
            "content": self._base_64_content,
            "isBase64Encoded": False,
            "encoding": DEFAULT_ENCODING,
            "created_time_epoch": self._unix_timestamp,
            "metadata": self._metadata,
            "ttl": self._ttl_timestamp,
        }

    def get_client_identifier(self):
        return self._metadata.get(KEY_CLIENT_ID)

    def _base64_decode_content(self, encoding: str = DEFAULT_ENCODING) -> str:
        base64_content_bytes = self._base_64_content.encode(encoding=encoding)
        content_bytes = base64.b64decode(base64_content_bytes)
        return content_bytes.decode(encoding=encoding)

    def _base64_encode_str(self, content: str, encoding: str = DEFAULT_ENCODING) -> str:
        b = base64.b64encode(bytes(content, encoding))
        return b.decode(encoding)

    def is_base64_encoded(self, content: str, encoding: str = DEFAULT_ENCODING) -> bool:
        try:
            decoded_content = base64.b64decode(content).decode(encoding)
            return (
                base64.b64encode(decoded_content.encode(encoding)).decode(encoding)
                == content
            )
        except Exception:
            return False
