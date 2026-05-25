from app.core.config import Settings
from app.providers.base import ImageProvider
from app.providers.image.imagen import ImagenProvider
from app.providers.image.mock import MockImageProvider


def build_image_provider(settings: Settings) -> ImageProvider:
    if settings.image_provider == "imagen" and settings.google_cloud_project:
        return ImagenProvider(settings)
    return MockImageProvider()
