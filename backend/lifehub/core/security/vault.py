import hvac
from sqlalchemy.orm import Session

from lifehub.config.constants import VAULT_ADDR, VAULT_TOKEN, VAULT_TRANSIT_MOUNT_POINT
from lifehub.core.common.base.service.base import BaseService


class VaultService(BaseService):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
        self.client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)

    def _generate_dek_and_encrypt(self, kek_path: str) -> str:
        """
        Generate a random data encryption key (DEK) and encrypt it
        using the key encryption key (KEK) specified by `kek_path`.
        """
        random_dek = self.client.secrets.transit.generate_data_key(
            name=kek_path, key_type="plaintext", mount_point=VAULT_TRANSIT_MOUNT_POINT
        )
        encrypted_dek: str = random_dek["data"]["ciphertext"]

        return encrypted_dek

    def _user_kek_exists(self, user_id: str) -> bool:
        """
        Check if a user's KEK exists by looking up the metadata in Vault KV.
        """
        try:
            existing_entry = self.client.secrets.kv.v2.read_secret_version(
                mount_point="kv/lifehub", path=f"user-keys/{user_id}"
            )
            return existing_entry is not None
        except hvac.exceptions.InvalidPath:
            return False  # No entry found, KEK does not exist

    def _generate_user_kek(self, user_id: str) -> None:
        """
        Create a user-specific KEK and track it in Vault KV.
        This assumes _user_kek_exists() has already been checked.
        """
        kek_name = f"user-{user_id}"

        if self._user_kek_exists(user_id):
            return

        # Create the KEK in Transit
        self.client.secrets.transit.create_key(
            name=kek_name, mount_point=VAULT_TRANSIT_MOUNT_POINT
        )

        # Store KEK metadata in Vault KV
        self.client.secrets.kv.v2.create_or_update_secret(
            mount_point="kv/lifehub",
            path=f"user-keys/{user_id}",
            secret={"kek_name": kek_name},
        )

    def generate_user_dek(self, user_id: str) -> str:
        """
        Generate a Data Encryption Key (DEK) for a user.
        Ensures the user's KEK exists before generating the DEK.
        """
        # This will create a new KEK if it doesn't exist
        self._generate_user_kek(user_id)
        return self._generate_dek_and_encrypt(f"user-{user_id}")

    def decrypt_data(self, encrypted_data: str, kek_path: str) -> str:
        """
        Decrypt the given encrypted data using the key encryption key (KEK)
        specified by `kek_name`.
        """
        result = self.client.secrets.transit.decrypt_data(
            name=kek_path,
            ciphertext=encrypted_data,
            mount_point=VAULT_TRANSIT_MOUNT_POINT,
        )

        decrypted_data: str = result["data"]["plaintext"]

        return decrypted_data
