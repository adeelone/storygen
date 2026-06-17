from pathlib import Path

from app.storage.local import LocalStorage


class MinIOStorage(LocalStorage):
    def __init__(self, root: Path, endpoint: str | None = None) -> None:
        super().__init__(root)
        self.endpoint = endpoint

    def signed_url(self, key: str, ttl_seconds: int) -> str:
        if not self.endpoint:
            return super().signed_url(key, ttl_seconds)
        return f"{self.endpoint.rstrip('/')}/{key}"
