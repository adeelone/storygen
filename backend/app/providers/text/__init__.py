from app.core.config import Settings
from app.providers.base import TextProvider
from app.providers.text.gemini import GeminiTextProvider
from app.providers.text.mock import MockTextProvider


def build_text_provider(settings: Settings) -> TextProvider:
    if settings.text_provider == "gemini" and settings.google_cloud_project:
        return GeminiTextProvider(settings)
    return MockTextProvider()
