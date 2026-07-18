from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.agents.pipeline import StoryPipeline
from app.agents.session_store import SessionEventStore
from app.api.routes import router as api_router
from app.api.websocket import router as ws_router
from app.core.config import Settings, get_settings
from app.core.logging import RequestIdMiddleware, configure_logging
from app.db import StoryRepository
from app.providers.image import build_image_provider
from app.providers.safety import RulesSafetyProvider
from app.providers.text import build_text_provider
from app.providers.tts import build_tts_provider
from app.storage.gcs import GCSStorage
from app.storage.local import LocalStorage
from app.storage.minio import MinIOStorage


def build_storage(settings: Settings, root: Path) -> LocalStorage:
    if settings.storage_provider == "gcs":
        return GCSStorage(root / "assets", settings.storage_bucket)
    if settings.storage_provider == "minio":
        return MinIOStorage(root / "assets", settings.storage_endpoint)
    return LocalStorage(root / "assets")


def create_app(data_root: Path | None = None) -> FastAPI:
    settings = get_settings().model_copy(deep=True)
    configure_logging(settings.log_json)
    root = data_root or Path(".data")
    storage = build_storage(settings, root)
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.state.data_root = root
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.repo = StoryRepository(root / "stories.json")
    app.state.settings = settings
    app.state.tts = build_tts_provider(settings)
    app.state.sessions = SessionEventStore()
    app.state.pipeline = StoryPipeline(
        build_text_provider(settings),
        build_image_provider(settings),
        RulesSafetyProvider(),
        storage,
        settings.session_image_budget,
        settings.signed_url_ttl_seconds,
    )
    app.mount("/assets", StaticFiles(directory=storage.root), name="assets")
    app.include_router(api_router, prefix=settings.api_prefix)
    app.include_router(ws_router)
    return app


app = create_app()
