import time
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime

from app.consistency import build_reference_prompt, build_scene_prompt, stable_seed
from app.core.errors import SafetyRefusal
from app.models import Scene, StoryRecord, StreamEvent
from app.providers.base import ImageProvider, SafetyProvider, TextProvider
from app.storage.local import LocalStorage

Emitter = Callable[[StreamEvent], Awaitable[None]]


class StoryPipeline:
    def __init__(
        self,
        text: TextProvider,
        image: ImageProvider,
        safety: SafetyProvider,
        storage: LocalStorage,
        image_budget: int = 8,
        signed_url_ttl_seconds: int = 900,
    ) -> None:
        self.text = text
        self.image = image
        self.safety = safety
        self.storage = storage
        self.image_budget = image_budget
        self.signed_url_ttl_seconds = signed_url_ttl_seconds

    def image_key(self, story_id: str, path: str, content_type: str) -> str:
        extension = "png" if content_type == "image/png" else "svg"
        return f"{story_id}/{path}.{extension}"

    async def generate(self, story: StoryRecord, emit: Emitter, cancelled: Callable[[], bool]) -> StoryRecord:
        started = time.perf_counter()
        safe, rewrite = await self.safety.screen(
            story.request.prompt + " " + " ".join(story.request.keywords), story.request.age_band.value
        )
        if not safe:
            raise SafetyRefusal("That idea is not suitable for this age setting.", rewrite or "Try a gentle adventure.")
        story.plan = await self.text.create_plan(story.request)
        await emit(
            StreamEvent(type="plan_ready", session_id=story.id, data={"plan": story.plan.model_dump(mode="json")})
        )

        image_count = 0
        for character in story.plan.characters:
            prompt = build_reference_prompt(character, story.plan.world.style_descriptor)
            generated = await self.image.render(prompt, stable_seed(story.id, character.id), "1:1")
            key = self.image_key(story.id, f"characters/{character.id}", generated.content_type)
            await self.storage.put(key, generated.content, generated.content_type)
            character.reference_url = self.storage.signed_url(key, self.signed_url_ttl_seconds)
            image_count += 1
            await emit(
                StreamEvent(
                    type="character_sheet", session_id=story.id, data={"character": character.model_dump(mode="json")}
                )
            )

        for outline in story.plan.scenes:
            if cancelled():
                story.status = "cancelled"
                return story
            scene = Scene(outline=outline)
            async for paragraph in self.text.stream_scene(story.plan, outline, story.request):
                safe, rewrite = await self.safety.screen(paragraph, story.request.age_band.value)
                if not safe:
                    raise SafetyRefusal("A generated passage needed a gentler rewrite.", rewrite or "Try again.")
                scene.paragraphs.append(paragraph)
                await emit(
                    StreamEvent(
                        type="scene_text", session_id=story.id, data={"scene": outline.number, "paragraph": paragraph}
                    )
                )
            scene.illustration_brief = f"{outline.location}: {outline.action}"
            scene.image_prompt = build_scene_prompt(story.plan, outline)
            if image_count < self.image_budget:
                reference = (
                    story.plan.characters[0].reference_url if self.image.supports_reference_conditioning else None
                )
                generated = await self.image.render(
                    scene.image_prompt,
                    stable_seed(story.id, story.plan.characters[0].id) + outline.number,
                    story.request.aspect_ratio.value,
                    reference,
                )
                key = self.image_key(story.id, f"scenes/{outline.number}", generated.content_type)
                await self.storage.put(key, generated.content, generated.content_type)
                scene.image_url = self.storage.signed_url(key, self.signed_url_ttl_seconds)
                image_count += 1
                await emit(
                    StreamEvent(
                        type="scene_image", session_id=story.id, data={"scene": outline.number, "url": scene.image_url}
                    )
                )
            story.scenes.append(scene)
            await emit(StreamEvent(type="scene_complete", session_id=story.id, data={"scene": outline.number}))
        story.status = "complete"
        story.completed_at = datetime.now(UTC)
        story.model_versions = {"text": self.text.model_name, "image": self.image.model_name}
        story.timing_ms = {"total": int((time.perf_counter() - started) * 1000)}
        story.estimated_cost_usd = round(image_count * 0.02 + len(story.scenes) * 0.001, 3)
        await emit(
            StreamEvent(type="story_complete", session_id=story.id, data={"story": story.model_dump(mode="json")})
        )
        return story

    async def regenerate_image(self, story: StoryRecord, scene_number: int, tweak: str) -> Scene:
        if not story.plan:
            raise ValueError("The story has no plan.")
        scene = next((scene for scene in story.scenes if scene.outline.number == scene_number), None)
        if not scene:
            raise ValueError("Scene not found.")
        scene.image_prompt = build_scene_prompt(story.plan, scene.outline) + f"\nSMALL TWEAK: {tweak}"
        generated = await self.image.render(
            scene.image_prompt,
            stable_seed(story.id, story.plan.characters[0].id) + scene_number,
            story.request.aspect_ratio.value,
            story.plan.characters[0].reference_url,
        )
        key = self.image_key(story.id, f"scenes/{scene_number}-reroll", generated.content_type)
        await self.storage.put(key, generated.content, generated.content_type)
        scene.image_url = self.storage.signed_url(key, self.signed_url_ttl_seconds)
        return scene

    async def regenerate_scene(self, story: StoryRecord, scene_number: int) -> Scene:
        if not story.plan:
            raise ValueError("The story has no plan.")
        scene = next((scene for scene in story.scenes if scene.outline.number == scene_number), None)
        if not scene:
            raise ValueError("Scene not found.")
        scene.paragraphs = [
            paragraph async for paragraph in self.text.stream_scene(story.plan, scene.outline, story.request)
        ]
        await self.regenerate_image(story, scene_number, "preserve character locks and refresh the composition")
        return scene
