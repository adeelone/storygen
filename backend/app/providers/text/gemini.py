import json
from collections.abc import AsyncIterator

from app.core.config import Settings
from app.models import PromptInput, SceneOutline, StoryPlan
from app.providers.text.mock import MockTextProvider


class GeminiTextProvider(MockTextProvider):
    """Vertex Gemini adapter with a deterministic mock fallback for local development.

    Production deployments can replace `_generate_json` and `_stream_text` with
    the Vertex SDK without changing agents or API routes.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.model_name = settings.gemini_model

    async def create_plan(self, request: PromptInput) -> StoryPlan:
        # The graph and validated schema stay active even before cloud credentials are mounted.
        return await super().create_plan(request)

    async def stream_scene(self, plan: StoryPlan, scene: SceneOutline, request: PromptInput) -> AsyncIterator[str]:
        async for paragraph in super().stream_scene(plan, scene, request):
            yield paragraph

    @staticmethod
    def structured_schema() -> str:
        return json.dumps(StoryPlan.model_json_schema())
