from dotenv import load_dotenv
import os


def get_db_connection_details():
    """
    Load and return database connection details from environment variables.
    """
    load_dotenv()

    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "schema_name": os.getenv("DB_SCHEMA", "public"),
    }
