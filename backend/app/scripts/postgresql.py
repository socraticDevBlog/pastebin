import asyncpg
import os
from dotenv import load_dotenv


async def create_paste_table(conn_details, schema_name):
    """
    Create the 'Paste' table in the database if it doesn't exist.
    """
    conn = await asyncpg.connect(**conn_details)

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.paste (
        id TEXT PRIMARY KEY,
        content TEXT NOT NULL,
        client_id TEXT NOT NULL,
        created_at BIGINT NOT NULL
    );
    """
    await conn.execute(create_table_query)
    print(
        f"Table 'paste' ensured in database {conn_details['database']} under schema {schema_name}."
    )

    await conn.close()


async def create_schema_if_not_exists(conn_details, schema_name):
    conn = await asyncpg.connect(**conn_details)

    query = f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
    await conn.execute(query)
    print(
        f"Schema '{schema_name}' ensured in database {conn_details['database']} under schema {schema_name}."
    )

    await conn.close()


if __name__ == "__main__":
    import asyncio

    load_dotenv()
    conn_details = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
    }
    schema_name = os.getenv("DB_SCHEMA", "public")
    asyncio.run(
        create_schema_if_not_exists(conn_details=conn_details, schema_name=schema_name)
    )
    asyncio.run(create_paste_table(conn_details=conn_details, schema_name=schema_name))
