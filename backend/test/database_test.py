from unittest.mock import AsyncMock, patch
from app.main import app

from fastapi import Depends

from fastapi.testclient import TestClient

import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

client = TestClient(app)  # Use FastAPI's TestClient for testing


@patch("app.main.initialize_database", new_callable=AsyncMock)
def test_app_initializes_database(mock_initialize_database):
    """
    Test that the app initializes the database when INIT_DB=true.
    """
    # Set the environment variable to simulate INIT_DB=true
    os.environ["INIT_DB"] = "true"
    client = TestClient(app)

    with client:
        pass

    # Assert that initialize_database was called
    mock_initialize_database.assert_called_once()


@patch("app.main.initialize_database", new_callable=AsyncMock)
def test_app_startup(mock_initialize_database):
    # Test that the app starts without initializing the database
    assert app  # Ensure the app instance is created
    mock_initialize_database.assert_not_called()


def get_db_connection():
    # Return a real or mock database connection
    pass


@app.get("/example")
async def example_route(db=Depends(get_db_connection)):
    # Use the db connection
    pass
