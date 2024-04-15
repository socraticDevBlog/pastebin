from dynamodb import DB
from abstract import Paste
from typing import Union


class PasteDataAware(Paste):
    """
    PasteDataAware

    Extension Paste class with database awareness
    """

    def __init__(
        self,
        db: DB,
        content: Union[str, bytes] = None,
        id: str = None,
        client_identifier: str = None,
    ):
        self._db = db
        super().__init__(id=id, content=content, client_identifier=client_identifier)

    def insert(self) -> str:
        """
        insert

        inserts a new Paste in database

        Returns:
            str: Paste's unique ID
        """
        return self._db.insert(self.dict())

    def read(self) -> str:
        """

        Args:
            none

        Returns:
            str: Paste content
        """

        return self._db.get_item(self.id)["Item"]["content"]
