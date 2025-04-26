from dotenv import load_dotenv
from app.services.db_client import DBClient
import os


def get_db_client():
    """
    Dependency to provide a DBClient instance.
    """

    load_dotenv()

    conn_details = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
    }
    schema_name = os.getenv("DB_SCHEMA", "public")
    return DBClient(conn_details, schema_name)
