from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.db_client import DBClient
from app.models import PasteDataAware

client = TestClient(app)


from unittest.mock import AsyncMock, patch
import asyncpg


@patch("app.services.db_client.asyncpg.connect", new_callable=AsyncMock)
@patch("app.services.dependencies.get_db_client", new_callable=AsyncMock)
def test_get_pastes(mock_get_db_client, mock_connect):
    # Mock the database connection
    mock_conn = AsyncMock()
    mock_connect.return_value = mock_conn

    # Mock the query results
    mock_conn.fetch.return_value = [
        {
            "content": "Test content 1",
            "paste_id": "123",
            "client_id": "test_client",
            "created_at": 1682515200,
        },
        {
            "content": "Test content 2",
            "paste_id": "456",
            "client_id": "test_client",
            "created_at": 1682515300,
        },
        {
            "content": "Test content 3",
            "paste_id": "789",
            "client_id": "test_client",
            "created_at": 1682515400,
        },
    ]

    # Mock the DBClient instance
    mock_db_client = mock_get_db_client.return_value

    # Make the GET request
    response = client.get("/api/v1/pastes", params={"client_id": "test_client"})
    assert response.status_code == 200

    # Assert the response contains the expected paste IDs
    assert response.json() == ["123", "456", "789"]

    # Ensure the mocked query was executed
    mock_conn.fetch.assert_called_once()
