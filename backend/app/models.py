from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator


class Vibe(str, Enum):
    cozy = "cozy"
    adventurous = "adventurous"
    silly = "silly"
    bedtime = "bedtime"


class AgeBand(str, Enum):
    young = "3-5"
    middle = "5-7"
    older = "7-9"


class StoryLength(str, Enum):
    short = "short"
    standard = "standard"
    long = "long"


class AspectRatio(str, Enum):
    square = "1:1"
    hero = "16:9"
    book = "3:4"


class PromptInput(BaseModel):
    prompt: str = ""
    keywords: list[str] = Field(default_factory=list, max_length=8)
    protagonists: list[str] = Field(default_factory=list, max_length=4)
    setting: str | None = None
    vibe: Vibe = Vibe.cozy
    age_band: AgeBand = AgeBand.middle
    length: StoryLength = StoryLength.standard
    moral: str | None = None
    language: str = "English"
    aspect_ratio: AspectRatio = AspectRatio.book
    style_preset: str = "watercolor"

    @model_validator(mode="after")
    def has_idea(self) -> "PromptInput":
        if not (self.prompt.strip() or self.keywords or self.protagonists):
            raise ValueError("Provide a prompt, keywords, or a protagonist.")
        return self


class Character(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    species: str
    age: str
    appearance_tokens: list[str]
    palette: list[str]
    clothing: str
    accessory: str
    distinguishing_mark: str
    personality: str
    signature_pose: str
    voice: str
    reference_url: str | None = None


class WorldBible(BaseModel):
    setting: str
    tone: str
    motifs: list[str]
    style_descriptor: str


class SceneOutline(BaseModel):
    number: int = Field(ge=1, le=4)
    arc: str
    title: str
    location: str
    character_ids: list[str]
    action: str
    emotional_beat: str


class StoryPlan(BaseModel):
    title: str
    world: WorldBible
    characters: list[Character]
    scenes: list[SceneOutline]

    @model_validator(mode="after")
    def four_scene_arc(self) -> "StoryPlan":
        expected = ["Setup", "Inciting Incident", "Climax", "Resolution"]
        if len(self.scenes) != 4 or [scene.arc for scene in self.scenes] != expected:
            raise ValueError("Story plan must contain the four narrative arc scenes.")
        return self


class Scene(BaseModel):
    outline: SceneOutline
    paragraphs: list[str] = Field(default_factory=list)
    illustration_brief: str = ""
    image_url: str | None = None
    image_prompt: str | None = None


class StoryRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    slug: str
    request: PromptInput
    plan: StoryPlan | None = None
    scenes: list[Scene] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
    public: bool = False
    share_expires_at: datetime | None = None
    model_versions: dict[str, str] = Field(default_factory=dict)
    timing_ms: dict[str, int] = Field(default_factory=dict)
    estimated_cost_usd: float = 0
    status: str = "draft"


class StreamEvent(BaseModel):
    type: str
    session_id: str
    data: dict[str, Any] = Field(default_factory=dict)
    emitted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
