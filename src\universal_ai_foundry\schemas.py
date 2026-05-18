from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class Modality(StrEnum):
    LLM = "llm"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"


class TrainingMethod(StrEnum):
    LORA = "lora"
    FULL_FINE_TUNE = "full_fine_tune"
    DREAMBOOTH = "dreambooth"
    DIFFUSION_LORA = "diffusion_lora"
    SPECTROGRAM_DIFFUSION = "spectrogram_diffusion"
    VIDEO_LORA = "video_lora"


class ResourceBudget(BaseModel):
    gpu_memory_gb: int = Field(default=12, ge=0, le=512)
    max_training_hours: int = Field(default=4, ge=1, le=720)
    mixed_precision: str = Field(default="bf16")
    gradient_checkpointing: bool = True


class DatasetSpec(BaseModel):
    path: Path
    format: str = Field(examples=["jsonl", "image-folder", "audio-folder", "video-folder"])
    license: str = "unknown"
    contains_personal_data: bool = False
    synthetic_allowed: bool = True


class ModelSpec(BaseModel):
    base_model: str
    output_dir: Path = Path("outputs")
    trust_remote_code: bool = False
    revision: str | None = None


class SafetyPolicy(BaseModel):
    allow_remote_code: bool = False
    require_dataset_license: bool = True
    block_secret_patterns: bool = True
    allow_network_downloads: bool = False
    require_human_review_before_run: bool = True


class CapsuleManifest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    version: str = "0.1.0"
    modality: Modality
    method: TrainingMethod
    description: str
    dataset: DatasetSpec
    model: ModelSpec
    resources: ResourceBudget = ResourceBudget()
    safety: SafetyPolicy = SafetyPolicy()
    training_arguments: dict[str, str | int | float | bool] = Field(default_factory=dict)
    commands: list[str] = Field(default_factory=list)

    @field_validator("commands")
    @classmethod
    def commands_must_be_non_empty(cls, commands: list[str]) -> list[str]:
        if not commands:
            raise ValueError("At least one training command template is required.")
        return commands


class SecurityFinding(BaseModel):
    severity: str
    code: str
    message: str


class ExecutionPlan(BaseModel):
    capsule_name: str
    modality: Modality
    method: TrainingMethod
    steps: list[str]
    estimated_gpu_memory_gb: int
    estimated_training_hours: int
    output_dir: Path
    warnings: list[str]


class BlueprintSummary(BaseModel):
    name: str
    modality: Modality
    method: TrainingMethod
    description: str


class ScaffoldRequest(BaseModel):
    target_name: str = Field(min_length=2, max_length=80)
    blueprint: str = "llm-lora"


class RunRequest(BaseModel):
    manifest: CapsuleManifest
    dry_run: bool = True


class RunResult(BaseModel):
    accepted: bool
    dry_run: bool
    commands: list[str]
    blocked_findings: list[SecurityFinding]

