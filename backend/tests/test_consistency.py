from app.consistency.prompts import build_scene_prompt
from app.consistency.seeds import stable_seed
from app.models import PromptInput
from app.providers.text.mock import MockTextProvider


async def test_plan_has_four_arc_scenes() -> None:
    plan = await MockTextProvider().create_plan(PromptInput(prompt="a brave squirrel"))
    assert [scene.arc for scene in plan.scenes] == ["Setup", "Inciting Incident", "Climax", "Resolution"]


async def test_prompt_locks_style_and_character_tokens() -> None:
    plan = await MockTextProvider().create_plan(PromptInput(prompt="a brave squirrel"))
    prompt = build_scene_prompt(plan, plan.scenes[0])
    assert "STYLE LOCK" in prompt
    assert "CHARACTER TOKEN LOCK" in prompt
    assert plan.characters[0].clothing in prompt


def test_seed_is_deterministic() -> None:
    assert stable_seed("story", "hero") == stable_seed("story", "hero")
    assert stable_seed("story", "hero") != stable_seed("story", "friend")


async def test_mock_provider_respects_language_and_length() -> None:
    request = PromptInput(prompt="una estrella", language="Spanish", length="short")
    provider = MockTextProvider()
    plan = await provider.create_plan(request)
    paragraphs = [paragraph async for paragraph in provider.stream_scene(plan, plan.scenes[0], request)]
    assert len(paragraphs) == 1
    assert "br\u00fajula" in paragraphs[0]
