from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_prefix="", extra="ignore")

    app_name: str = "StoryGen API"
    app_env: Literal["development", "test", "production"] = "development"
    api_prefix: str = "/api/v1"
    frontend_url: str = "http://localhost:3000"
    database_url: str = "sqlite:///./storygen.db"
    redis_url: str = "redis://localhost:6379/0"
    storage_provider: Literal["local", "gcs", "minio"] = "local"
    storage_bucket: str = "storygen-assets"
    storage_endpoint: str | None = None
    google_cloud_project: str | None = None
    google_cloud_location: str = "us-central1"
    text_provider: Literal["mock", "gemini"] = "mock"
    image_provider: Literal["mock", "imagen"] = "mock"
    tts_provider: Literal["mock", "gcp"] = "mock"
    safety_provider: Literal["rules", "mock"] = "rules"
    gemini_model: str = "gemini-1.5-flash"
    imagen_model: str = "imagen-3.0-generate-002"
    session_token_budget: int = 7000
    session_image_budget: int = 8
    anonymous_daily_quota: int = 5
    signed_url_ttl_seconds: int = 900
    enable_tts: bool = True
    enable_eval_dashboard: bool = True
    enable_public_sharing: bool = True
    enable_pdf_export: bool = True
    log_json: bool = False
    admin_key: str | None = Field(default=None, repr=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
