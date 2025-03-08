import logging

import hvac

from lifehub.config.constants import cfg

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_vault() -> None:
    """
    Setup Vault with the necessary secrets engines, roles, and policies.
    """

    try:
        # Initialize Vault client
        client = hvac.Client(url=cfg.VAULT_ADDR, token=cfg.VAULT_TOKEN)

        sys_backend = client.sys

        ## --- Transit Engine for Lifehub ---
        transit_engines = sys_backend.list_mounted_secrets_engines()  # type: ignore
        if "transit/lifehub/" not in transit_engines:
            client.sys.enable_secrets_engine(
                backend_type="transit",
                path="transit/lifehub",
            )
            logger.info("Transit secrets engine for Lifehub enabled.")

        ## --- KV Secret Engine for Lifehub ---
        kv_engines = sys_backend.list_mounted_secrets_engines()  # type: ignore
        if "kv/lifehub/" not in kv_engines:
            client.sys.enable_secrets_engine(
                backend_type="kv",
                path="kv/lifehub",
                options={"version": "2"},
            )
            logger.info("KV-v2 secrets engine for Lifehub enabled.")

        ## --- Database Secret Engine for Lifehub ---
        database_engines = sys_backend.list_mounted_secrets_engines()  # type: ignore
        if cfg.VAULT_DB_MOUNT_POINT + "/" not in database_engines:
            client.sys.enable_secrets_engine(
                backend_type="database",
                path=cfg.VAULT_DB_MOUNT_POINT,
            )
            logger.info("Database secrets engine for Lifehub enabled.")

        # Configure the database secret engine (only if not already configured)
        try:
            client.secrets.database.read_connection(
                name=cfg.DB_NAME, mount_point=cfg.VAULT_DB_MOUNT_POINT
            )
            logger.info("Database connection already configured.")
        except hvac.exceptions.InvalidPath:
            client.secrets.database.configure(
                name=cfg.DB_NAME,
                plugin_name="mysql-database-plugin",
                mount_point=cfg.VAULT_DB_MOUNT_POINT,
                connection_url="{{username}}:{{password}}@tcp("
                + cfg.DB_HOST
                + ":3306)/",
                allowed_roles=[cfg.VAULT_DB_ROLE, cfg.VAULT_DB_ADMIN_ROLE],
                username=cfg.VAULT_DB_USER,
                password=cfg.VAULT_DB_PASSWORD,
            )
            logger.info("Database connection configured in Vault.")

        # Create a read/write role for the database secret engine
        try:
            existing_roles = client.secrets.database.list_roles(
                mount_point=cfg.VAULT_DB_MOUNT_POINT
            )
        except hvac.exceptions.InvalidPath:
            existing_roles = {"data": {"keys": []}}

        if cfg.VAULT_DB_ROLE not in existing_roles["data"]["keys"]:
            client.secrets.database.create_role(
                name=cfg.VAULT_DB_ROLE,
                db_name=cfg.DB_NAME,
                mount_point=cfg.VAULT_DB_MOUNT_POINT,
                creation_statements=[
                    "CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}';",
                    "GRANT SELECT, INSERT, UPDATE, DELETE ON "
                    + cfg.DB_NAME
                    + ".* TO '{{name}}'@'%';",
                ],
                default_ttl="1h",
                max_ttl="24h",
            )
            logger.info(f"Database role '{cfg.VAULT_DB_ROLE}' created.")

        # Create an admin role for the database secret engine
        if cfg.VAULT_DB_ADMIN_ROLE not in existing_roles["data"]["keys"]:
            client.secrets.database.create_role(
                name=cfg.VAULT_DB_ADMIN_ROLE,
                db_name=cfg.DB_NAME,
                mount_point=cfg.VAULT_DB_MOUNT_POINT,
                creation_statements=[
                    "CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}';",
                    "GRANT ALL PRIVILEGES ON " + cfg.DB_NAME + ".* TO '{{name}}'@'%';",
                    "GRANT GRANT OPTION ON " + cfg.DB_NAME + ".* TO '{{name}}'@'%';",
                ],
                default_ttl="1h",
                max_ttl="2h",
            )
            logger.info(f"Database admin role '{cfg.VAULT_DB_ADMIN_ROLE}' created.")

        # Setup Vault policies for access control
        setup_vault_policies(client)

    except Exception as e:
        logger.error(f"Error setting up Vault: {e}")
        raise


def setup_vault_policies(client: hvac.Client) -> None:
    """
    Configure Vault policies to enforce security and access control.

    - `user-keystore` policy: Restricts each user to encrypt and decrypt their own data.
    - `backend-keystore` policy: Grants the backend full access to all user keys.

    These policies ensure:
    1. Users can only encrypt/decrypt using their own KEK.
    2. Users cannot list or modify other users' KEKs.
    3. The backend has full control over all KEKs for encryption management.
    """

    # Policy for regular users (per-user restricted access)
    user_policy = """
    # Allow users to encrypt data using only their own KEK
    path "transit/lifehub/encrypt/user-{{identity.entity.id}}" {
        capabilities = ["update"]
    }

    # Allow users to decrypt data using only their own KEK
    path "transit/lifehub/decrypt/user-{{identity.entity.id}}" {
        capabilities = ["update"]
    }

    # Allow users to read metadata about their own KEK from Vault KV
    path "kv/lifehub/user-keys/{{identity.entity.id}}" {
        capabilities = ["read"]
    }
    """

    # Policy for the backend service (full access to all user KEKs)
    backend_policy = """
    # Backend can encrypt data using any user's KEK
    path "transit/lifehub/encrypt/user-*" {
        capabilities = ["update"]
    }

    # Backend can decrypt data using any user's KEK
    path "transit/lifehub/decrypt/user-*" {
        capabilities = ["update"]
    }

    # Backend can create, update, read, and delete user KEKs
    path "transit/lifehub/keys/user-*" {
        capabilities = ["create", "update", "read", "delete"]
    }

    # Backend has full access to all user KEK metadata in Vault KV
    path "kv/lifehub/user-keys/*" {
        capabilities = ["create", "update", "read", "delete"]
    }
    """

    # Apply the policies in Vault
    client.sys.create_or_update_policy(name="user-keystore", policy=user_policy)
    client.sys.create_or_update_policy(name="backend-keystore", policy=backend_policy)

    logger.info("Vault policies configured successfully.")
