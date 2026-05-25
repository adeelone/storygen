from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass

from app.models import PromptInput, SceneOutline, StoryPlan


@dataclass
class GeneratedImage:
    content: bytes
    content_type: str
    metadata: dict[str, str]


class TextProvider(ABC):
    model_name: str

    @abstractmethod
    async def create_plan(self, request: PromptInput) -> StoryPlan: ...

    @abstractmethod
    def stream_scene(self, plan: StoryPlan, scene: SceneOutline, request: PromptInput) -> AsyncIterator[str]: ...


class ImageProvider(ABC):
    model_name: str
    supports_reference_conditioning: bool = False

    @abstractmethod
    async def render(
        self, prompt: str, seed: int, aspect_ratio: str, reference_url: str | None = None
    ) -> GeneratedImage: ...


class TTSProvider(ABC):
    @abstractmethod
    async def narrate(self, text: str, language: str) -> bytes: ...


class SafetyProvider(ABC):
    @abstractmethod
    async def screen(self, text: str, age_band: str) -> tuple[bool, str | None]: ...
