import hvac

from lifehub.config.constants import (
    DB_HOST,
    DB_NAME,
    VAULT_ADDR,
    VAULT_DB_PASSWORD,
    VAULT_DB_ROLE,
    VAULT_DB_USER,
    VAULT_TOKEN,
)


def setup_vault() -> None:
    # Initialize Vault client
    client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)

    sys_backend = client.sys
    # Enable the Transit secret engine if not already enabled
    transit_engines = sys_backend.list_mounted_secrets_engines()  # type: ignore
    if "transit/" not in transit_engines:
        client.sys.enable_secrets_engine(
            backend_type="transit",
            path="transit",
        )
        print("Transit secrets engine enabled.")

    # Enable the kv-v2 secret engine if not already enabled
    kv_engines = sys_backend.list_mounted_secrets_engines()  # type: ignore
    if "kv/" not in kv_engines:
        client.sys.enable_secrets_engine(
            backend_type="kv",
            path="kv",
            options={"version": "2"},
        )
        print("KV-v2 secrets engine enabled.")

    # Enable the database secret engine if not already enabled
    database_engines = sys_backend.list_mounted_secrets_engines()  # type: ignore
    if "database/" not in database_engines:
        client.sys.enable_secrets_engine(
            backend_type="database",
            path="database",
        )
        print("Database secrets engine enabled.")

    # Configure the database secret engine
    client.secrets.database.configure(
        name=DB_NAME,
        plugin_name="mysql-database-plugin",
        connection_url=f"{VAULT_DB_USER}:{VAULT_DB_PASSWORD}@tcp({DB_HOST}:3306)/",
        allowed_roles=VAULT_DB_ROLE,
    )

    # Define the role
    client.secrets.database.create_or_update_role(
        name=VAULT_DB_ROLE,
        db_name=DB_NAME,
        creation_statements=[
            "CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}';",
            "GRANT SELECT ON " + DB_NAME + ".* TO '{{name}}'@'%';",
        ],
        default_ttl="1h",
        max_ttl="24h",
    )
