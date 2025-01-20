import hvac
from sqlalchemy.orm import Session

from lifehub.config.constants import VAULT_ADDR, VAULT_TOKEN
from lifehub.core.common.base.service.base import BaseService


class VaultService(BaseService):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
        self.client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)

    def _generate_encrypted_dek(self, kek_name: str) -> str:
        """
        Generate a random data encryption key (DEK) and encrypt it
        using the key encryption key (KEK) specified by `kek_name`.
        """
        random_dek = self.client.secrets.transit.generate_data_key(
            name=kek_name, key_type="plaintext"
        )
        encrypted_dek: str = random_dek["data"]["ciphertext"]

        return encrypted_dek

    def _generate_user_kek(self, user_id: str) -> None:
        """
        Generate a random key encryption key (KEK) for a user.
        """
        kek_name = f"user-{user_id}"
        self.client.secrets.transit.create_key(name=kek_name)

    def generate_user_dek(self, user_id: str) -> str:
        """
        Generate a random data encryption key (DEK) for a user.
        """
        kek_name = f"user-{user_id}"
        self._generate_user_kek(user_id)
        return self._generate_encrypted_dek(kek_name)

    def decrypt_data(self, encrypted_data: str, kek_name: str) -> str:
        """
        Decrypt the given encrypted data using the key encryption key (KEK)
        specified by `kek_name`.
        """
        result = self.client.secrets.transit.decrypt_data(
            name=kek_name, ciphertext=encrypted_data
        )

        decrypted_data: str = result["data"]["plaintext"]

        return decrypted_data
