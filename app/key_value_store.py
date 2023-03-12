from dataclasses import dataclass
from time import time
from typing import Optional


@dataclass
class Value:
    value: str
    expires_at: Optional[int]


class KeyValueStore:
    store: dict[str, Value]

    def __init__(self) -> None:
        self.store = {}

    def set(self, key: str, value: str, *,
            expiry_ms: Optional[int] = None,
            expiry_sec: Optional[int] = None,
            expires_at_sec: Optional[int] = None,
            expires_at_ms: Optional[int] = None) -> None:
        if expiry_ms is not None:
            expires_at_ms = int(time() * 1000) + expiry_ms
        if expiry_sec is not None:
            expires_at_sec = int(time()) + expiry_sec
        if expires_at_sec is not None:
            expires_at_ms = expires_at_sec * 1000
        self.store[key] = Value(value, expires_at_ms)

    def get(self, key: str) -> Optional[str]:
        if key not in self.store:
            return None
        value = self.store[key]
        if value.expires_at is not None and value.expires_at < int(time() * 1000):
            del self.store[key]
            return None
        return value.value
