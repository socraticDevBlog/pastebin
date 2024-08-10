from dynamodb import DB
from typing import List


class ApiHandlerException(Exception):
    def __init__(self, message="ApiHandler encountered an error"):
        self.message = message
        super().__init__(self.message)


class ApiHandler:
    def __init__(self, db: DB, base_url: str) -> None:
        self._db = db
        self._base_url = base_url

    def latest_pastes_urls(
        self, limit: int = 5, client_identifier: str = None
    ) -> List[str]:
        try:
            pastes_id = self._db.paste_ids_by_client_identifier(
                client_identifier=client_identifier, count=limit
            )
        except:
            raise ApiHandlerException()

        urls = [f"{self._base_url}/paste?id={id}" for id in pastes_id]

        return urls
