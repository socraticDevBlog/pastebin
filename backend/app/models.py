import time
from typing import Optional

from pydantic import BaseModel, Field

from app.utils import from_base64, is_base64, to_base64


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

    def __init__(
        self,
        content: str,
        client_id: str,
        created_at: Optional[int] = None,
        paste_id: str = None,
    ):
        self.paste_id = paste_id
        self._content = content if is_base64(content) else to_base64(content)
        self.client_id = client_id
        self.created_at = int(time.time()) if created_at is None else created_at

    @property
    def encoded_content(self) -> str:
        """
        Get the decoded content of the paste.

        Returns:
            str: The decoded content of the paste.
        """
        return self._content if is_base64(self._content) else to_base64(self._content)

    @property
    def plain_content(self) -> str:
        """
        Get the plain content of the paste.

        Returns:
            str: The plain content of the paste.
        """
        return (
            self._content
            if not is_base64(self._content)
            else from_base64(self._content)
        )
