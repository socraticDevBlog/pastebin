import time
from typing import Optional

from pydantic import BaseModel
from app.utils import hash_value


class PasteModel(BaseModel):
    """
    Paste model for creating and retrieving pastes
    with FastAPI.

    Attributes:
        content (str): Content of the paste.
        workspace (Optional[str]): Optional workspace identifier.
    """

    content: str
    workspace: Optional[str]


class PasteDataAware:
    """
    Paste data model for creating and retrieving pastes
    with actual database

    Attributes:
        id (str): Unique identifier for the paste.
        content (str): Content of the paste.
        client_id (str): Identifier for the client creating the paste.
        created_at (int): Timestamp of when the paste was created.
    """

    id: str
    content: str
    client_id: str
    created_at: int

    def __init__(
        self,
        content: str,
        client_id: str,
        created_at: Optional[int] = None,
        id: str = None,
    ):
        self.id = hash_value(value=content) if id is None else id
        self.content = content
        self.client_id = client_id
        self.created_at = int(time.time()) if created_at is None else created_at
