from app.core.config import Settings
from app.providers.base import TextProvider
from app.providers.text.gemini import GeminiTextProvider
from app.providers.text.mock import MockTextProvider


def build_text_provider(settings: Settings) -> TextProvider:
    if settings.text_provider == "gemini":
        if not settings.google_cloud_project:
            if settings.app_env == "production":
                raise RuntimeError("GOOGLE_CLOUD_PROJECT is required when TEXT_PROVIDER=gemini.")
            return MockTextProvider()
        return GeminiTextProvider(settings)
    return MockTextProvider()
