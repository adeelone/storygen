import json
from asyncio import to_thread
from collections.abc import AsyncIterator

from app.core.config import Settings
from app.models import PromptInput, SceneOutline, StoryPlan
from app.providers.text.mock import MockTextProvider


class GeminiTextProvider(MockTextProvider):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.model_name = settings.gemini_model
        try:
            import vertexai
            from vertexai.generative_models import GenerationConfig, GenerativeModel
        except ImportError as exc:
            raise RuntimeError("Install backend[cloud] to use TEXT_PROVIDER=gemini.") from exc
        vertexai.init(project=settings.google_cloud_project, location=settings.google_cloud_location)
        self._config = GenerationConfig(response_mime_type="application/json")
        self._model = GenerativeModel(settings.gemini_model)

    async def create_plan(self, request: PromptInput) -> StoryPlan:
        prompt = (
            "Create a children's story plan as JSON matching this schema. "
            "Use exactly four scenes with arcs Setup, Inciting Incident, Climax, Resolution. "
            "Include stable visual appearance tokens for every character.\n"
            f"Schema: {self.structured_schema()}\n"
            f"Request: {request.model_dump_json()}"
        )
        response = await to_thread(self._model.generate_content, prompt, generation_config=self._config)
        return StoryPlan.model_validate_json(response.text)

    async def stream_scene(self, plan: StoryPlan, scene: SceneOutline, request: PromptInput) -> AsyncIterator[str]:
        prompt = (
            "Write only the prose for this one children's story scene. "
            "Return 2 to 4 short paragraphs separated by blank lines. "
            f"Language: {request.language}. Age band: {request.age_band.value}. "
            f"Story plan: {plan.model_dump_json()}. Scene: {scene.model_dump_json()}"
        )
        response = await to_thread(self._model.generate_content, prompt)
        for paragraph in [part.strip() for part in response.text.split("\n\n") if part.strip()]:
            yield paragraph

    @staticmethod
    def structured_schema() -> str:
        return json.dumps(StoryPlan.model_json_schema())
