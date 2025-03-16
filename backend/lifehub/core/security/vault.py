import hvac
from sqlalchemy.orm import Session

from lifehub.config.constants import cfg
from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.user.schema import User


class VaultServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Vault", status_code, message)


class VaultService(BaseUserService):
    """
    This class shouldn't be used directly.
    Instead, use the EncryptionService, which provides a higher-level API.
    """

    def __init__(self, session: Session, user: User) -> None:
        super().__init__(session, user)
        self.client = hvac.Client(url=cfg.VAULT_ADDR, token=cfg.VAULT_TOKEN)
        self.kek_path = f"user-{self.user.id}"

    def _user_kek_exists(self) -> bool:
        """
        Check if a user's KEK exists by looking up the metadata in Vault KV.
        """
        try:
            existing_entry = self.client.secrets.kv.v2.read_secret_version(
                mount_point="kv/lifehub", path=f"user-keys/{self.user.id}"
            )
            return existing_entry is not None
        except hvac.exceptions.InvalidPath:
            return False  # No entry found, KEK does not exist

    def _generate_user_kek(self) -> None:
        """
        Create a user-specific KEK and track it in Vault KV.
        This assumes _user_kek_exists() has already been checked.
        """
        # Create the KEK in Transit
        self.client.secrets.transit.create_key(
            name=self.kek_path, mount_point=cfg.VAULT_TRANSIT_MOUNT_POINT
        )

        # Store KEK metadata in Vault KV
        self.client.secrets.kv.v2.create_or_update_secret(
            mount_point="kv/lifehub",
            path=f"user-keys/{self.user.id}",
            secret={"kek_name": self.kek_path},
        )

    def _encrypt_user_dek(self, dek: str) -> str:
        """
        Encrypt the Data Encryption Key (DEK) using the user's KEK.
        The DEK should be encoded as base64.
        """
        result = self.client.secrets.transit.encrypt_data(
            name=self.kek_path,
            plaintext=dek,
            mount_point=cfg.VAULT_TRANSIT_MOUNT_POINT,
        )
        return result["data"]["ciphertext"]  # type: ignore

    def encrypt_user_dek(self, dek: str) -> str:
        """
        Generate a Data Encryption Key (DEK) for a user.
        Ensures the user's KEK exists before generating the DEK.
        """
        # This will create a new KEK if it doesn't exist
        if not self._user_kek_exists():
            self._generate_user_kek()
        return self._encrypt_user_dek(dek)

    def decrypt_user_dek(self, encrypted_dek: str) -> str:
        """
        Decrypt the Data Encryption Key (DEK) using the user's KEK.
        """
        result = self.client.secrets.transit.decrypt_data(
            name=self.kek_path,
            ciphertext=encrypted_dek,
            mount_point=cfg.VAULT_TRANSIT_MOUNT_POINT,
        )
        return result["data"]["plaintext"]  # type: ignore
