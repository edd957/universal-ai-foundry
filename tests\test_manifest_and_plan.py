from pathlib import Path

from universal_ai_foundry.io import load_manifest
from universal_ai_foundry.planner import build_plan


def test_load_manifest_and_build_plan() -> None:
    manifest = load_manifest(Path("examples/llm_lora_capsule.json"))
    plan = build_plan(manifest)

    assert plan.capsule_name == "example-llm-lora"
    assert plan.modality.value == "llm"
    assert plan.steps

