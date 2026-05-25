from app.providers.base import TTSProvider


class MockTTSProvider(TTSProvider):
    async def narrate(self, text: str, language: str) -> bytes:
        return f"StoryGen narration preview ({language}): {text}".encode()
