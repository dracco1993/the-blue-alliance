from oauth2client import client as client, transport as transport
from typing import Any, Optional

METADATA_ROOT: Any
METADATA_HEADERS: Any

def get(http: Any, path: Any, root: Any = ..., recursive: Optional[Any] = ...): ...
def get_service_account_info(http: Any, service_account: str = ...): ...
def get_token(http: Any, service_account: str = ...): ...
