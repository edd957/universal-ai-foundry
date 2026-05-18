from __future__ import annotations

import re
from pathlib import Path

from universal_ai_foundry.schemas import CapsuleManifest, SecurityFinding

SECRET_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"api[_-]?key",
        r"secret",
        r"token",
        r"password",
        r"-----BEGIN (RSA|OPENSSH|PRIVATE) KEY-----",
    ]
]

RISKY_COMMAND_PATTERNS = [
    "curl ",
    "wget ",
    "rm -rf",
    "chmod 777",
    "sudo ",
    "powershell -enc",
]


def review_manifest(manifest: CapsuleManifest, root: Path | None = None) -> list[SecurityFinding]:
    findings: list[SecurityFinding] = []
    root = root or Path.cwd()
    _check_paths(manifest, root, findings)
    _check_remote_code(manifest, findings)
    _check_dataset_policy(manifest, findings)
    _check_resources(manifest, findings)
    _check_commands(manifest, findings)
    return findings


def _check_paths(manifest: CapsuleManifest, root: Path, findings: list[SecurityFinding]) -> None:
    for label, path in {
        "dataset.path": manifest.dataset.path,
        "model.output_dir": manifest.model.output_dir,
    }.items():
        if path.is_absolute() or ".." in path.parts:
            findings.append(
                SecurityFinding(
                    severity="high",
                    code="PATH_TRAVERSAL",
                    message=f"{label} must stay inside the capsule workspace: {path}",
                )
            )
        resolved = (root / path).resolve()
        if root.resolve() not in resolved.parents and resolved != root.resolve():
            findings.append(
                SecurityFinding(
                    severity="medium",
                    code="OUTSIDE_WORKSPACE",
                    message=f"{label} resolves outside the workspace: {resolved}",
                )
            )


def _check_remote_code(manifest: CapsuleManifest, findings: list[SecurityFinding]) -> None:
    if manifest.model.trust_remote_code and not manifest.safety.allow_remote_code:
        findings.append(
            SecurityFinding(
                severity="critical",
                code="REMOTE_CODE_BLOCKED",
                message="Model requests trust_remote_code while capsule policy blocks it.",
            )
        )


def _check_dataset_policy(manifest: CapsuleManifest, findings: list[SecurityFinding]) -> None:
    if manifest.dataset.license == "unknown" and manifest.safety.require_dataset_license:
        findings.append(
            SecurityFinding(
                severity="medium",
                code="DATASET_LICENSE_UNKNOWN",
                message="Dataset license must be reviewed before training.",
            )
        )
    if manifest.dataset.contains_personal_data:
        findings.append(
            SecurityFinding(
                severity="high",
                code="PERSONAL_DATA_REVIEW",
                message="Dataset indicates personal data and requires privacy review.",
            )
        )


def _check_resources(manifest: CapsuleManifest, findings: list[SecurityFinding]) -> None:
    if manifest.resources.max_training_hours > 24:
        findings.append(
            SecurityFinding(
                severity="medium",
                code="LONG_RUNNING_JOB",
                message="Training job exceeds 24 hours and should be explicitly approved.",
            )
        )
    if manifest.resources.gpu_memory_gb > 80:
        findings.append(
            SecurityFinding(
                severity="low",
                code="LARGE_GPU_BUDGET",
                message="GPU memory request is unusually high for a local capsule.",
            )
        )


def _check_commands(manifest: CapsuleManifest, findings: list[SecurityFinding]) -> None:
    for command in manifest.commands:
        lower = command.lower()
        for risky_pattern in RISKY_COMMAND_PATTERNS:
            if risky_pattern in lower:
                findings.append(
                    SecurityFinding(
                        severity="high",
                        code="RISKY_COMMAND",
                        message=(
                            f"Command contains risky pattern "
                            f"'{risky_pattern.strip()}': {command}"
                        ),
                    )
                )
        if manifest.safety.block_secret_patterns:
            for secret_pattern in SECRET_PATTERNS:
                if secret_pattern.search(command):
                    findings.append(
                        SecurityFinding(
                            severity="high",
                            code="SECRET_PATTERN",
                            message=f"Command appears to contain a secret-like token: {command}",
                        )
                    )
