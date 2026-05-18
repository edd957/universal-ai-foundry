from universal_ai_foundry.io import load_manifest
from universal_ai_foundry.scaffold import scaffold_capsule


def test_scaffold_capsule_creates_manifest(tmp_path) -> None:
    manifest_path = scaffold_capsule(tmp_path / "my-llm", "llm-lora")
    manifest = load_manifest(manifest_path)

    assert manifest.name == "my-llm"
    assert (tmp_path / "my-llm" / "datasets" / ".gitkeep").exists()

