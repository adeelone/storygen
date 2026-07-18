from app.providers.base import TTSProvider


class GCPTTSProvider(TTSProvider):
    model_name = "google-cloud-text-to-speech"
    content_type = "audio/mpeg"

    async def narrate(self, text: str, language: str) -> bytes:
        try:
            from google.cloud import texttospeech
        except ImportError as exc:
            raise RuntimeError("Install backend[cloud] to use TTS_PROVIDER=gcp.") from exc

        language_code = "es-ES" if language.lower().startswith("spanish") else "en-US"
        client = texttospeech.TextToSpeechAsyncClient()
        response = await client.synthesize_speech(
            request=texttospeech.SynthesizeSpeechRequest(
                input=texttospeech.SynthesisInput(text=text),
                voice=texttospeech.VoiceSelectionParams(
                    language_code=language_code,
                    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
                ),
                audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3),
            )
        )
        return bytes(response.audio_content)
