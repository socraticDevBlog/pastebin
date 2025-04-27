import asyncpg

from app.models import PasteDataAware


class DBClient:
    def __init__(self, conn_details, schema_name="public"):
        """
        Initialize the DBClient with connection details and schema name.
        """
        self.conn_details = conn_details
        self.schema_name = schema_name

    async def get_pastes(self, client_id: str) -> list[PasteDataAware]:
        """
        Retrieve pastes for a specific client.

        Args:
            client_id (str): The client ID to filter pastes.

        Returns:
            list: A list of PasteDataAware objects.
        """
        conn = await asyncpg.connect(**self.conn_details)

        try:
            query = f"""
            SELECT content, paste_id, client_id, created_at
            FROM {self.schema_name}.paste
            WHERE client_id = $1
            ORDER BY created_at DESC;
            """
            results = await conn.fetch(query, client_id)

            return [
                PasteDataAware(
                    content=result["content"],
                    paste_id=str(result["paste_id"]),
                    client_id=result["client_id"],
                    created_at=result["created_at"],
                )
                for result in results
            ]
        finally:
            await conn.close()

    async def get_paste(self, id: str) -> PasteDataAware:
        """
        Retrieve a paste by its ID.

        Args:
            id (str): The ID of the paste to retrieve.

        Returns:
            PasteDataAware: a Paste filled with all its database informations.
        """
        conn = await asyncpg.connect(**self.conn_details)

        try:
            query = f"""
            SELECT content, paste_id, client_id, created_at
            FROM {self.schema_name}.paste
            WHERE paste_id = $1;
            """
            result = await conn.fetchrow(query, id)

            if result:
                return PasteDataAware(
                    content=result["content"],
                    paste_id=str(result["paste_id"]),
                    client_id=result["client_id"],
                    created_at=result["created_at"],
                )
            else:
                return None
        finally:
            await conn.close()

    async def insert_paste(self, paste: PasteDataAware) -> str:
        """
        Insert a new paste into the 'paste' table.

        Args:
            content (str): The content of the paste.
            client_id (str): The client ID associated with the paste.
            created_at (int): The timestamp when the paste was created.

        Returns:
            str: the UUID of the paste.
        """
        conn = await asyncpg.connect(**self.conn_details)

        try:
            insert_query = f"""
            INSERT INTO {self.schema_name}.paste (content, client_id, created_at)
            VALUES ($1, $2, $3)
            RETURNING id, paste_id;
            """
            result = await conn.fetchrow(
                insert_query, paste.base64_content(), paste.client_id, paste.created_at
            )

            return result["paste_id"]
        finally:
            await conn.close()
