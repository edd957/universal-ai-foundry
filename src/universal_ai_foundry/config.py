from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for local AI Capsule orchestration."""

    model_config = SettingsConfigDict(env_prefix="UAF_", env_file=".env", extra="ignore")

    env: str = "local"
    workspace: Path = Field(default=Path("runs"))
    allow_remote_code: bool = False
    max_gpu_memory_gb: int = 24
    max_training_hours: int = 12


@lru_cache
def get_settings() -> Settings:
    return Settings()

