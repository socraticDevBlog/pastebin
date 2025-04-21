from dotenv import load_dotenv
import os
from app.scripts.postgresql import create_schema_if_not_exists, create_paste_table


async def initialize_database():
    """
    Initialize the database by creating the schema and table if they don't exist.
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

    # Ensure schema and table exist
    await create_schema_if_not_exists(
        conn_details=conn_details, schema_name=schema_name
    )
    await create_paste_table(conn_details=conn_details, schema_name=schema_name)
