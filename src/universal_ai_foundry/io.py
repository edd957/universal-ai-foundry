from __future__ import annotations

import json
from pathlib import Path

from universal_ai_foundry.schemas import CapsuleManifest


def load_manifest(path: Path) -> CapsuleManifest:
    data = json.loads(path.read_text(encoding="utf-8"))
    return CapsuleManifest.model_validate(data)


def write_manifest(path: Path, manifest: CapsuleManifest) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        manifest.model_dump_json(indent=2),
        encoding="utf-8",
    )

