from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM LoRA training recipe placeholder.")
    parser.add_argument("--capsule", required=True)
    args = parser.parse_args()
    manifest = json.loads(Path(args.capsule).read_text(encoding="utf-8"))
    output_dir = Path(manifest["model"]["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "TRAINING_PLAN.md").write_text(
        "# LLM LoRA Training Plan\n\nInstall `.[llm]` and replace this recipe with "
        "your organization-approved training implementation.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

