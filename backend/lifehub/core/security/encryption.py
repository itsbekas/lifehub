import base64
import hashlib
import hmac
import os
from typing import overload

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sqlalchemy.orm import Session

from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.security.vault import VaultService
from lifehub.core.user.schema import User


class EncryptionServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Encryption", status_code, message)


class EncryptionService(BaseUserService):
    # Lazy load
    _user_data_key: str | None = None
    _aesgcm: AESGCM | None = None

    def __init__(self, session: Session, user: User) -> None:
        super().__init__(session, user)
        self.vault = VaultService(session, user)

    @property
    def user_data_key(self) -> str:
        if self._user_data_key is None:
            self._user_data_key = self.vault.decrypt_user_dek(self.user.data_key)
        return self._user_data_key

    @property
    def aesgcm(self) -> AESGCM:
        if self._aesgcm is None:
            self._aesgcm = AESGCM(base64.b64decode(self.user_data_key))
        return self._aesgcm

    def _bytes_to_str(self, data: bytes) -> str:
        return base64.b64encode(data).decode("utf-8")

    def _generate_random_bytes(self, length: int) -> bytes:
        """
        Generate a random byte string of the specified length.
        """
        return os.urandom(length)

    def _generate_aes_nonce(self) -> bytes:
        """
        Generate a random 96-bit AES nonce.
        """
        return self._generate_random_bytes(12)

    def _generate_aes_key(self) -> bytes:
        """
        Generate a random 256-bit AES key.
        """
        return AESGCM.generate_key(256)

    def generate_encrypted_data_key(self) -> str:
        """
        Generate a random data encryption key (DEK) and encrypt it
        using the user's key encryption key (KEK).
        """
        data_key: str = self._bytes_to_str(self._generate_aes_key())
        return self.vault.encrypt_user_dek(data_key)

    @overload
    def encrypt_data(self, data: str) -> bytes: ...

    @overload
    def encrypt_data(self, data: None) -> None: ...

    def encrypt_data(self, data: str | None) -> bytes | None:
        """
        Encrypt the given data using a random DEK and AES-GCM.
        """
        if data is None:
            return None

        key_version = 1  # Placeholder until key rotation is implemented
        nonce = self._generate_aes_nonce()
        ciphertext = self.aesgcm.encrypt(nonce, data.encode("utf-8"), None)

        return bytes([key_version]) + nonce + ciphertext

    @overload
    def decrypt_data(self, data: bytes) -> str: ...

    @overload
    def decrypt_data(self, data: None) -> None: ...

    def decrypt_data(self, data: bytes | None) -> str | None:
        """
        Decrypt the given data using the user's DEK and AES-GCM.
        """
        if data is None:
            return None

        # key_version = data[0]
        nonce = data[1:13]
        ciphertext = data[13:]

        return self.aesgcm.decrypt(
            nonce,
            ciphertext,
            None,
        ).decode("utf-8")

    @staticmethod
    def hmac(text: str, secret_key: str) -> str:
        """
        Returns an HMAC-SHA256 hash of the text using the given secret key.
        Text is normalized to lowercase and stripped of whitespace.
        """
        normalized_text = text.strip().lower().encode("utf-8")
        secret_key_bytes = secret_key.encode("utf-8")
        digest = hmac.new(secret_key_bytes, normalized_text, hashlib.sha256).hexdigest()
        return digest
