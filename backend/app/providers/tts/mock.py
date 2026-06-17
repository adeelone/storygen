from app.providers.base import TTSProvider


class MockTTSProvider(TTSProvider):
    content_type = "audio/wav"

    async def narrate(self, text: str, language: str) -> bytes:
        import io
        import math
        import wave

        duration = max(0.4, min(3.0, len(text.split()) * 0.08))
        sample_rate = 16_000
        frames = int(sample_rate * duration)
        output = io.BytesIO()
        with wave.open(output, "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(sample_rate)
            for index in range(frames):
                envelope = 0.25 if index < frames * 0.9 else max(0.0, (frames - index) / (frames * 0.1)) * 0.25
                value = int(32767 * envelope * math.sin(2 * math.pi * 440 * index / sample_rate))
                audio.writeframesraw(value.to_bytes(2, "little", signed=True))
        return output.getvalue()
