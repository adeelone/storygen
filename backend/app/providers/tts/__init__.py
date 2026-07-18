from app.core.config import Settings
from app.providers.base import TTSProvider
from app.providers.tts.gcp_tts import GCPTTSProvider
from app.providers.tts.mock import MockTTSProvider


def build_tts_provider(settings: Settings) -> TTSProvider:
    if settings.tts_provider == "gcp":
        if not settings.google_cloud_project:
            if settings.app_env == "production":
                raise RuntimeError("GOOGLE_CLOUD_PROJECT is required when TTS_PROVIDER=gcp.")
            return MockTTSProvider()
        return GCPTTSProvider()
    return MockTTSProvider()


__all__ = ["GCPTTSProvider", "MockTTSProvider", "build_tts_provider"]
