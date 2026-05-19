from __future__ import annotations

from pathlib import Path

from cryptography.fernet import Fernet

from app.core.config.settings import get_settings


def _get_or_create_key(key_file: Path) -> bytes:
    key_file.parent.mkdir(parents=True, exist_ok=True)
    if key_file.exists():
        return key_file.read_bytes()
    key = Fernet.generate_key()
    key_file.write_bytes(key)
    key_file.chmod(0o600)
    return key


def _resolve_key(*, key: bytes | None, key_file: Path | None) -> bytes:
    if key is not None:
        return key
    settings = get_settings()
    if settings.encryption_key is not None:
        return settings.encryption_key.encode("ascii")
    resolved_file = key_file or settings.encryption_key_file
    return _get_or_create_key(resolved_file)


class TokenEncryptor:
    def __init__(self, key: bytes | None = None, key_file: Path | None = None) -> None:
        resolved_key = _resolve_key(key=key, key_file=key_file)
        self._fernet = Fernet(resolved_key)

    def encrypt(self, token: str) -> bytes:
        return self._fernet.encrypt(token.encode())

    def decrypt(self, encrypted: bytes) -> str:
        return self._fernet.decrypt(encrypted).decode()


def get_or_create_key(key_file: Path | None = None) -> bytes:
    return _resolve_key(key=None, key_file=key_file)
