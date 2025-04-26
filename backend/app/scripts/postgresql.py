import asyncpg


async def create_schema_if_not_exists(conn_details, schema_name):
    """
    Create the schema in the database if it doesn't exist.
    """
    conn = await asyncpg.connect(**conn_details)

    query = f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
    await conn.execute(query)
    print(f"Schema '{schema_name}' ensured in database '{conn_details['database']}'.")

    await conn.close()


async def create_paste_table(conn_details, schema_name):
    """
    Create the 'Paste' table in the database if it doesn't exist.
    """
    conn = await asyncpg.connect(**conn_details)

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.paste (
        id SERIAL PRIMARY KEY,  -- Auto-incrementing integer
        paste_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,  -- Unique GUID
        content TEXT NOT NULL,
        client_id TEXT NOT NULL,
        created_at BIGINT NOT NULL
    );
    """
    # Ensure the pgcrypto extension is enabled for UUID generation
    await conn.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
    await conn.execute(create_table_query)
    print(
        f"Table 'paste' ensured in database {conn_details['database']} under schema {schema_name}."
    )

    await conn.close()
