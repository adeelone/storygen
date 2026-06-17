from datetime import timedelta
from pathlib import Path

from app.storage.local import LocalStorage


class GCSStorage(LocalStorage):
    def __init__(self, root: Path, bucket_name: str) -> None:
        super().__init__(root)
        try:
            from google.cloud import storage
        except ImportError as exc:
            raise RuntimeError("Install backend[cloud] to use STORAGE_PROVIDER=gcs.") from exc
        self._bucket = storage.Client().bucket(bucket_name)

    async def put(self, key: str, content: bytes, content_type: str) -> str:
        blob = self._bucket.blob(key)
        blob.upload_from_string(content, content_type=content_type)
        return key

    def signed_url(self, key: str, ttl_seconds: int) -> str:
        return str(
            self._bucket.blob(key).generate_signed_url(
                expiration=timedelta(seconds=ttl_seconds),
                method="GET",
            )
        )
