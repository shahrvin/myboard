import json
from typing import Any

from cryptography.fernet import Fernet
from sqlalchemy import String, Text
from sqlalchemy.types import TypeDecorator

from app.config import settings


def _get_fernet() -> Fernet:
    return Fernet(settings.DB_ENCRYPTION_KEY.encode())


class EncryptedString(TypeDecorator):
    """Stores a string as Fernet-encrypted bytes in a TEXT column."""

    impl = Text
    cache_ok = True

    def process_bind_param(self, value: str | None, dialect: Any) -> str | None:
        if value is None:
            return None
        return _get_fernet().encrypt(value.encode()).decode()

    def process_result_value(self, value: str | None, dialect: Any) -> str | None:
        if value is None:
            return None
        return _get_fernet().decrypt(value.encode()).decode()


class EncryptedJSON(TypeDecorator):
    """Stores a dict/list as Fernet-encrypted JSON in a TEXT column."""

    impl = Text
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Any) -> str | None:
        if value is None:
            return None
        return _get_fernet().encrypt(json.dumps(value).encode()).decode()

    def process_result_value(self, value: str | None, dialect: Any) -> Any:
        if value is None:
            return None
        return json.loads(_get_fernet().decrypt(value.encode()).decode())
