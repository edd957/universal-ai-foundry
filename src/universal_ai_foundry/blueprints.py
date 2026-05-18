from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from universal_ai_foundry.schemas import (
    BlueprintSummary,
    CapsuleManifest,
    DatasetSpec,
    Modality,
    ModelSpec,
    ResourceBudget,
    SafetyPolicy,
    TrainingMethod,
)


BLUEPRINTS: dict[str, CapsuleManifest] = {
    "llm-lora": CapsuleManifest(
        name="llm-lora-starter",
        modality=Modality.LLM,
        method=TrainingMethod.LORA,
        description="Parameter-efficient local LLM fine-tuning with LoRA adapters.",
        dataset=DatasetSpec(
            path=Path("datasets/instructions.jsonl"),
            format="jsonl",
            license="unknown",
        ),
        model=ModelSpec(
            base_model="local-or-huggingface/base-llm",
            output_dir=Path("outputs/llm-lora"),
        ),
        resources=ResourceBudget(gpu_memory_gb=16, max_training_hours=6),
        safety=SafetyPolicy(),
        training_arguments={"learning_rate": 0.0002, "epochs": 3, "rank": 16},
        commands=[
            "python recipes/llm_lora_train.py --capsule capsule.json",
            "python recipes/export_adapter.py --capsule capsule.json",
        ],
    ),
    "image-diffusion-lora": CapsuleManifest(
        name="image-diffusion-lora-starter",
        modality=Modality.IMAGE,
        method=TrainingMethod.DIFFUSION_LORA,
        description="Local text-to-image diffusion LoRA training capsule.",
        dataset=DatasetSpec(
            path=Path("datasets/images"),
            format="image-folder",
            license="unknown",
        ),
        model=ModelSpec(
            base_model="local-or-huggingface/base-diffusion",
            output_dir=Path("outputs/image"),
        ),
        resources=ResourceBudget(gpu_memory_gb=12, max_training_hours=5),
        safety=SafetyPolicy(),
        training_arguments={"learning_rate": 0.0001, "steps": 1000, "resolution": 768},
        commands=[
            "python recipes/image_lora_train.py --capsule capsule.json",
            "python recipes/export_safetensors.py --capsule capsule.json",
        ],
    ),
    "music-generator": CapsuleManifest(
        name="music-generator-starter",
        modality=Modality.AUDIO,
        method=TrainingMethod.SPECTROGRAM_DIFFUSION,
        description="Audio generation capsule using spectrogram-based local training.",
        dataset=DatasetSpec(
            path=Path("datasets/audio"),
            format="audio-folder",
            license="unknown",
        ),
        model=ModelSpec(base_model="local/audio-base", output_dir=Path("outputs/music")),
        resources=ResourceBudget(gpu_memory_gb=16, max_training_hours=8),
        safety=SafetyPolicy(),
        training_arguments={"sample_rate": 44100, "clip_seconds": 10, "steps": 2000},
        commands=[
            "python recipes/audio_prepare.py --capsule capsule.json",
            "python recipes/music_train.py --capsule capsule.json",
        ],
    ),
    "video-diffusion-lora": CapsuleManifest(
        name="video-diffusion-lora-starter",
        modality=Modality.VIDEO,
        method=TrainingMethod.VIDEO_LORA,
        description="Video generation capsule for short video diffusion adapter training.",
        dataset=DatasetSpec(
            path=Path("datasets/videos"),
            format="video-folder",
            license="unknown",
        ),
        model=ModelSpec(base_model="local/video-base", output_dir=Path("outputs/video")),
        resources=ResourceBudget(gpu_memory_gb=24, max_training_hours=12),
        safety=SafetyPolicy(),
        training_arguments={"frames": 16, "resolution": 512, "steps": 1500},
        commands=[
            "python recipes/video_prepare.py --capsule capsule.json",
            "python recipes/video_lora_train.py --capsule capsule.json",
        ],
    ),
}


def list_blueprints() -> list[BlueprintSummary]:
    return [
        BlueprintSummary(
            name=name,
            modality=manifest.modality,
            method=manifest.method,
            description=manifest.description,
        )
        for name, manifest in BLUEPRINTS.items()
    ]


def get_blueprint(name: str) -> CapsuleManifest:
    if name not in BLUEPRINTS:
        available = ", ".join(sorted(BLUEPRINTS))
        raise KeyError(f"Unknown blueprint '{name}'. Available: {available}")
    return deepcopy(BLUEPRINTS[name])
