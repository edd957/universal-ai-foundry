from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

from universal_ai_foundry.schemas import CapsuleManifest, RunResult
from universal_ai_foundry.security import review_manifest


class LocalRunner:
    """Small guarded local runner for capsule command templates."""

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace

    def run(self, manifest: CapsuleManifest, dry_run: bool = True) -> RunResult:
        findings = review_manifest(manifest, self.workspace)
        blocking = [finding for finding in findings if finding.severity in {"critical", "high"}]
        if blocking:
            return RunResult(
                accepted=False,
                dry_run=dry_run,
                commands=manifest.commands,
                blocked_findings=blocking,
            )

        if dry_run:
            return RunResult(
                accepted=True,
                dry_run=True,
                commands=manifest.commands,
                blocked_findings=[],
            )

        for command in manifest.commands:
            subprocess.run(
                shlex.split(command),
                cwd=self.workspace,
                check=True,
                shell=False,
            )
        return RunResult(
            accepted=True,
            dry_run=False,
            commands=manifest.commands,
            blocked_findings=[],
        )

