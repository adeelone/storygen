import base64
from asyncio import to_thread

from app.core.config import Settings
from app.providers.base import GeneratedImage
from app.providers.image.mock import MockImageProvider


class ImagenProvider(MockImageProvider):
    supports_reference_conditioning = True

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.model_name = settings.imagen_model
        try:
            import vertexai
            from vertexai.preview.vision_models import ImageGenerationModel
        except ImportError as exc:
            raise RuntimeError("Install backend[cloud] to use IMAGE_PROVIDER=imagen.") from exc
        vertexai.init(project=settings.google_cloud_project, location=settings.google_cloud_location)
        self._model = ImageGenerationModel.from_pretrained(settings.imagen_model)

    async def render(
        self, prompt: str, seed: int, aspect_ratio: str, reference_url: str | None = None
    ) -> GeneratedImage:
        def generate() -> GeneratedImage:
            result = self._model.generate_images(
                prompt=prompt,
                number_of_images=1,
                aspect_ratio=aspect_ratio,
                seed=seed,
                safety_filter_level="block_some",
            )
            image = result.images[0]
            data = getattr(image, "_image_bytes", None) or base64.b64decode(image._as_base64_string())
            return GeneratedImage(data, "image/png", {"seed": str(seed), "reference_url": reference_url or ""})

        return await to_thread(generate)
