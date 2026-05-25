from app.storage.local import LocalStorage


class MinIOStorage(LocalStorage):
    """S3-compatible MinIO boundary; local behavior keeps CI credential free."""
