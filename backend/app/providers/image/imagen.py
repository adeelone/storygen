from app.core.config import Settings
from app.providers.base import GeneratedImage
from app.providers.image.mock import MockImageProvider


class ImagenProvider(MockImageProvider):
    """Imagen-compatible adapter boundary.

    The local fallback makes development and CI deterministic; a deployed
    provider implementation can replace `render` with Vertex AI output.
    """

    supports_reference_conditioning = True

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.model_name = settings.imagen_model

    async def render(
        self, prompt: str, seed: int, aspect_ratio: str, reference_url: str | None = None
    ) -> GeneratedImage:
        return await super().render(prompt, seed, aspect_ratio, reference_url)
