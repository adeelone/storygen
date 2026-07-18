from app.core.config import Settings
from app.providers.base import ImageProvider
from app.providers.image.imagen import ImagenProvider
from app.providers.image.mock import MockImageProvider


def build_image_provider(settings: Settings) -> ImageProvider:
    if settings.image_provider == "imagen":
        if not settings.google_cloud_project:
            if settings.app_env == "production":
                raise RuntimeError("GOOGLE_CLOUD_PROJECT is required when IMAGE_PROVIDER=imagen.")
            return MockImageProvider()
        return ImagenProvider(settings)
    return MockImageProvider()
