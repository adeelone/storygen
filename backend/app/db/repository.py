import json
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock

from app.models import StoryRecord


class StoryRepository:
    """Small JSON repository for local/dev operation.

    The interface is deliberately storage-neutral so Cloud SQL/SQLAlchemy can
    be introduced behind it without disturbing API or pipeline code.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _read(self) -> list[StoryRecord]:
        return [StoryRecord.model_validate(row) for row in json.loads(self.path.read_text(encoding="utf-8"))]

    def _write(self, stories: list[StoryRecord]) -> None:
        self.path.write_text(
            json.dumps([story.model_dump(mode="json") for story in stories], indent=2),
            encoding="utf-8",
        )

    def save(self, story: StoryRecord) -> StoryRecord:
        with self._lock:
            stories = [existing for existing in self._read() if existing.id != story.id]
            stories.insert(0, story)
            self._write(stories)
        return story

    def get(self, story_id: str) -> StoryRecord | None:
        with self._lock:
            return next((story for story in self._read() if story.id == story_id), None)

    def get_by_slug(self, slug: str) -> StoryRecord | None:
        with self._lock:
            return next((story for story in self._read() if story.slug == slug), None)

    def list(self, query: str = "", vibe: str | None = None, language: str | None = None) -> list[StoryRecord]:
        with self._lock:
            stories = self._read()
        needle = query.lower()
        return [
            story
            for story in stories
            if (not needle or needle in story.slug.lower() or needle in story.request.prompt.lower())
            and (not vibe or story.request.vibe.value == vibe)
            and (not language or story.request.language == language)
        ]

    def usage_summary(self) -> dict[str, float | int]:
        stories = self.list()
        today = datetime.now(UTC).date()
        daily = [story for story in stories if story.created_at.date() == today]
        return {
            "stories_today": len(daily),
            "images_today": sum(
                len(story.scenes) + (len(story.plan.characters) if story.plan else 0) for story in daily
            ),
            "estimated_cost_usd_today": round(sum(story.estimated_cost_usd for story in daily), 4),
        }
