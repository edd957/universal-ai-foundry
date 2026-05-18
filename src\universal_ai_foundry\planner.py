from __future__ import annotations

from universal_ai_foundry.schemas import CapsuleManifest, ExecutionPlan


def build_plan(manifest: CapsuleManifest) -> ExecutionPlan:
    warnings: list[str] = []
    if manifest.dataset.license == "unknown" and manifest.safety.require_dataset_license:
        warnings.append("Dataset license is unknown and must be reviewed before training.")
    if manifest.model.trust_remote_code and not manifest.safety.allow_remote_code:
        warnings.append("Model requests remote code, but safety policy blocks remote code.")
    if manifest.resources.gpu_memory_gb == 0:
        warnings.append("CPU-only training may be too slow for most generative workloads.")

    steps = [
        "Validate capsule manifest.",
        "Run security review.",
        f"Prepare dataset from {manifest.dataset.path}.",
        f"Load base model {manifest.model.base_model}.",
        f"Execute {manifest.method.value} training workflow.",
        f"Write artifacts to {manifest.model.output_dir}.",
        "Generate training report and reproducibility metadata.",
    ]
    return ExecutionPlan(
        capsule_name=manifest.name,
        modality=manifest.modality,
        method=manifest.method,
        steps=steps,
        estimated_gpu_memory_gb=manifest.resources.gpu_memory_gb,
        estimated_training_hours=manifest.resources.max_training_hours,
        output_dir=manifest.model.output_dir,
        warnings=warnings,
    )

