from hashlib import sha256
from pathlib import Path


class LocalStorage:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    async def put(self, key: str, content: bytes, content_type: str) -> str:
        path = self.root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return key

    def signed_url(self, key: str, ttl_seconds: int) -> str:
        signature = sha256(f"{key}:{ttl_seconds}:storygen-local".encode()).hexdigest()[:16]
        return f"/assets/{key}?expires={ttl_seconds}&signature={signature}"
