from dataclasses import dataclass
from time import time
from typing import Optional


@dataclass
class Value:
    value: str
    expiry_ms: Optional[int]
    insert_time: int


class KeyValueStore:
    store: dict[str, Value]

    def __init__(self):
        self.store = {}

    def set(self, key: str, value: str, expiry_ms: Optional[int] = None):
        self.store[key] = Value(value, expiry_ms, int(time() * 1000))

    def get(self, key: str) -> Optional[str]:
        if key in self.store:
            value = self.store[key]
            # check expiry
            if value.expiry_ms is not None:
                current_ms = int(time() * 1000)
                if current_ms - value.insert_time > value.expiry_ms:
                    # key expired
                    del self.store[key]
                    return None
            return value.value
        else:
            return None
