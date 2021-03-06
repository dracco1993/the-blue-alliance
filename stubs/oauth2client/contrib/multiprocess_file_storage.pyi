from oauth2client import client as client
from typing import Any

INTERPROCESS_LOCK_DEADLINE: int
logger: Any

class _MultiprocessStorageBackend:
    def __init__(self, filename: Any) -> None: ...
    def acquire_lock(self) -> None: ...
    def release_lock(self) -> None: ...
    def locked_get(self, key: Any): ...
    def locked_put(self, key: Any, credentials: Any) -> None: ...
    def locked_delete(self, key: Any) -> None: ...

class MultiprocessFileStorage(client.Storage):
    def __init__(self, filename: Any, key: Any) -> None: ...
    def acquire_lock(self) -> None: ...
    def release_lock(self) -> None: ...
    def locked_get(self): ...
    def locked_put(self, credentials: Any): ...
    def locked_delete(self): ...
