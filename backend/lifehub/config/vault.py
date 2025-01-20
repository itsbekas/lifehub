import hvac

from lifehub.config.constants import VAULT_ADDR, VAULT_TOKEN


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
