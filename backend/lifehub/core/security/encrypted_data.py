from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.types import String, TypeDecorator

if TYPE_CHECKING:
    from sqlalchemy import Dialect


class EncryptedDataType(TypeDecorator[str]):
    impl = String(128)

    def process_bind_param(self, value: str | None, dialect: Dialect) -> str | None:
        """
        This method is called before data is persisted to the database.
        It checks that the value adheres to the expected "key_version;nonce;ciphertext" format.
        """
        if value is None:
            return value

        # Check the value is a string and matches the expected format
        if isinstance(value, str):
            parts = value.split(";")
            if len(parts) != 3:
                raise ValueError(
                    "Invalid encrypted data format. Expected format: key_version;nonce;ciphertext"
                )
        else:
            raise TypeError("Encrypted data must be stored as a string.")

        return value

    def process_result_value(self, value: str | None, dialect: Dialect) -> str | None:
        """
        This method is called when data is loaded from the database.
        You can optionally validate or transform the data here.
        """
        return value  # You might choose to leave it as-is.
