from app.services.db_client import DBClient
from app.db_configs import get_db_connection_details


def get_db_client():
    """
    Dependency to provide a DBClient instance.
    """
    conn_details = get_db_connection_details()
    schema_name = conn_details.pop("schema_name")
    return DBClient(conn_details, schema_name)
