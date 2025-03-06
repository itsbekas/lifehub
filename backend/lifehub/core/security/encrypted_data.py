from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy.types import VARBINARY, TypeDecorator

if TYPE_CHECKING:
    pass


class EncryptedDataType(TypeDecorator[bytes]):
    """
    A SQLAlchemy TypeDecorator for encrypted data.
    It is used to store encrypted data as binary data in the database.
    The format of the data is as follows:
    - key_version (1 byte)
    - nonce (12 bytes)
    - ciphertext (variable length)
    The constructor takes the length of the ciphertext in bytes,
    but the total size of the data is 1 + 12 + ciphertext_length.
    """

    cache_ok = True  # This is required to allow TypeDecorator to be cached

    def __init__(
        self, ciphertext_length: int, *args: list[Any], **kwargs: dict[Any, Any]
    ) -> None:
        """
        Initializes the encrypted data type.

        :param ciphertext_length: Length of the ciphertext in bytes.
        """
        self.ciphertext_length = ciphertext_length
        total_size = (
            1 + 12 + ciphertext_length + 16
        )  # key_version(1) + nonce(12) + ciphertext + tag(16)
        # Dynamically set the VARBINARY size
        # Needs to be done at the class level because that's what SQLAlchemy checks
        # (see TypeDecorator)
        self.__class__.impl = VARBINARY(
            total_size
        )  # Dynamically set the VARBINARY size
        super().__init__(*args, **kwargs)
