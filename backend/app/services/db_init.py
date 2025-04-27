from app.scripts.postgresql import create_schema_if_not_exists, create_paste_table
from app.db_configs import get_db_connection_details


async def initialize_database():
    """
    Initialize the database by creating the schema and table if they don't exist.
    """
    conn_details = get_db_connection_details()
    schema_name = conn_details.pop("schema_name")

    # Ensure schema and table exist
    await create_schema_if_not_exists(
        conn_details=conn_details, schema_name=schema_name
    )
    await create_paste_table(conn_details=conn_details, schema_name=schema_name)
