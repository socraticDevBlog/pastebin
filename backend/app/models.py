import base64
import time
from typing import Optional

from pydantic import BaseModel, Field


class PasteInputModel(BaseModel):
    """
    Input model for creating a new paste.
    """

    content: str
    workspace: Optional[str] = ""


class PasteModel(PasteInputModel):
    """
    Model for retrieving pastes, including the paste_id.
    """

    paste_id: Optional[str]


class PasteDataAware:
    """
    Paste data model for creating and retrieving pastes
    with actual database

    Attributes:
        paste_id (str): Unique paste_identifier for the paste.
        content (str): Content of the paste.
        client_id (str): paste_identifier for the client creating the paste.
        created_at (int): Timestamp of when the paste was created.
    """

    paste_id: str
    content: str
    client_id: str
    created_at: int
    content_encoding: str = Field(
        default="utf-8",
        description="Encoding used for the content. Default is 'utf-8'.",
    )

    def __init__(
        self,
        content: str,
        client_id: str,
        created_at: Optional[int] = None,
        paste_id: str = None,
        content_encoding: str = "utf-8",
    ):
        self.paste_id = paste_id
        self._content = (
            content
            if self._is_base64(content)
            else base64.b64encode(content.encode(content_encoding)).decode(
                content_encoding
            )
        )
        self.client_id = client_id
        self.created_at = int(time.time()) if created_at is None else created_at
        self.content_encoding = content_encoding

    def _is_base64(self, s: str) -> bool:
        """
        Check if a string is valid Base64.

        Args:
            s (str): The string to check.

        Returns:
            bool: True if the string is valid Base64, False otherwise.
        """
        try:
            # Decode and re-encode to verify Base64 validity
            return base64.b64encode(base64.b64decode(s)).decode("utf-8") == s
        except Exception:
            return False

    def plain_content(self):
        """
        Returns the content of the paste in plain text format.

        """
        return base64.b64decode(self._content.encode(self.content_encoding)).decode(
            self.content_encoding
        )

    def base64_content(self):
        """
        Returns the content of the paste in base64 format.

        """
        return self._content
