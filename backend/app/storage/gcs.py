from app.storage.local import LocalStorage


class GCSStorage(LocalStorage):
    """Storage boundary for GCS signed objects; local behavior is used in development."""
