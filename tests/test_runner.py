from universal_ai_foundry.blueprints import get_blueprint
from universal_ai_foundry.runner import LocalRunner


def test_runner_blocks_high_severity_findings(tmp_path) -> None:
    manifest = get_blueprint("llm-lora")
    manifest.model.trust_remote_code = True
    runner = LocalRunner(tmp_path)

    result = runner.run(manifest, dry_run=True)

    assert result.accepted is False
    assert result.blocked_findings


def test_runner_accepts_safe_dry_run(tmp_path) -> None:
    manifest = get_blueprint("llm-lora")
    manifest.dataset.license = "cc-by-4.0"
    runner = LocalRunner(tmp_path)

    result = runner.run(manifest, dry_run=True)

    assert result.accepted is True
    assert result.dry_run is True

