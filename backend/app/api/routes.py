import re
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from pathlib import Path

from fastapi import APIRouter, Header, HTTPException, Request, Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from pydantic import BaseModel

from app.agents.pipeline import StoryPipeline
from app.db import StoryRepository
from app.eval.runner import run_eval
from app.exports import render_epub, render_pdf
from app.models import PromptInput, StoryRecord

router = APIRouter()


class ImageReroll(BaseModel):
    tweak: str = "make the light warmer"


class ShareRequest(BaseModel):
    expires_days: int | None = 30


def dependencies(request: Request) -> tuple[StoryRepository, StoryPipeline]:
    return request.app.state.repo, request.app.state.pipeline


def check_admin(request: Request, admin_key: str | None) -> None:
    expected = request.app.state.settings.admin_key
    if expected and admin_key != expected:
        raise HTTPException(403, "Administrator access required")


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/stories", response_model=StoryRecord)
async def create_story(payload: PromptInput, request: Request) -> StoryRecord:
    repo, _ = dependencies(request)
    if repo.count_today() >= request.app.state.settings.anonymous_daily_quota:
        raise HTTPException(HTTP_429_TOO_MANY_REQUESTS, "Daily anonymous story quota reached.")
    base = re.sub(r"[^a-z0-9]+", "-", (payload.prompt or "-".join(payload.keywords) or "story").lower()).strip("-")[:38]
    story = StoryRecord(id=str(uuid4()), slug=f"{base or 'story'}-{uuid4().hex[:6]}", request=payload)
    return repo.save(story)


@router.get("/stories", response_model=list[StoryRecord])
async def list_stories(
    request: Request, q: str = "", vibe: str | None = None, language: str | None = None
) -> list[StoryRecord]:
    repo, _ = dependencies(request)
    return repo.list(q, vibe, language)


@router.get("/stories/{story_id}", response_model=StoryRecord)
async def get_story(story_id: str, request: Request) -> StoryRecord:
    repo, _ = dependencies(request)
    story = repo.get(story_id)
    if not story:
        raise HTTPException(404, "Story not found")
    return story


@router.post("/stories/{story_id}/share", response_model=StoryRecord)
async def share_story(story_id: str, payload: ShareRequest, request: Request) -> StoryRecord:
    repo, _ = dependencies(request)
    story = repo.get(story_id)
    if not story:
        raise HTTPException(404, "Story not found")
    story.public = True
    story.share_expires_at = datetime.now(UTC) + timedelta(days=payload.expires_days) if payload.expires_days else None
    return repo.save(story)


@router.delete("/stories/{story_id}/share", response_model=StoryRecord)
async def revoke_share(story_id: str, request: Request) -> StoryRecord:
    repo, _ = dependencies(request)
    story = repo.get(story_id)
    if not story:
        raise HTTPException(404, "Story not found")
    story.public = False
    return repo.save(story)


@router.get("/shares/{slug}", response_model=StoryRecord)
async def public_story(slug: str, request: Request) -> StoryRecord:
    repo, _ = dependencies(request)
    story = repo.get_by_slug(slug)
    expired = story and story.share_expires_at and story.share_expires_at < datetime.now(UTC)
    if not story or not story.public or expired:
        raise HTTPException(404, "Shared story not found")
    return story


@router.post("/stories/{story_id}/scenes/{scene_number}/image", response_model=StoryRecord)
async def reroll_image(story_id: str, scene_number: int, payload: ImageReroll, request: Request) -> StoryRecord:
    repo, pipeline = dependencies(request)
    story = repo.get(story_id)
    if not story:
        raise HTTPException(404, "Story not found")
    await pipeline.regenerate_image(story, scene_number, payload.tweak)
    return repo.save(story)


@router.post("/stories/{story_id}/scenes/{scene_number}/regenerate", response_model=StoryRecord)
async def regenerate_scene(story_id: str, scene_number: int, request: Request) -> StoryRecord:
    repo, pipeline = dependencies(request)
    story = repo.get(story_id)
    if not story:
        raise HTTPException(404, "Story not found")
    await pipeline.regenerate_scene(story, scene_number)
    return repo.save(story)


@router.get("/stories/{story_id}/export.pdf")
async def pdf(story_id: str, request: Request) -> Response:
    repo, _ = dependencies(request)
    story = repo.get(story_id)
    if not story:
        raise HTTPException(404, "Story not found")
    return Response(render_pdf(story), media_type="application/pdf")


@router.get("/stories/{story_id}/export.epub")
async def epub(story_id: str, request: Request) -> Response:
    repo, _ = dependencies(request)
    story = repo.get(story_id)
    if not story:
        raise HTTPException(404, "Story not found")
    return Response(render_epub(story), media_type="application/epub+zip")


@router.get("/admin/usage")
async def usage(request: Request, x_admin_key: str | None = Header(default=None)) -> dict[str, float | int]:
    check_admin(request, x_admin_key)
    repo, _ = dependencies(request)
    return repo.usage_summary()


@router.get("/admin/eval")
async def evaluation(request: Request, x_admin_key: str | None = Header(default=None)) -> dict[str, object]:
    check_admin(request, x_admin_key)
    return await run_eval(Path("reports"))


@router.post("/stories/{story_id}/narration")
async def narration(story_id: str, request: Request) -> Response:
    repo, _ = dependencies(request)
    story = repo.get(story_id)
    if not story:
        raise HTTPException(404, "Story not found")
    text = " ".join(paragraph for scene in story.scenes for paragraph in scene.paragraphs)
    tts = request.app.state.tts
    audio = await tts.narrate(text, story.request.language)
    return Response(audio, media_type=tts.content_type)
