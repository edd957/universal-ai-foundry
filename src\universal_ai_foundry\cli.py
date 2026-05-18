from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from universal_ai_foundry.api.main import app as fastapi_app
from universal_ai_foundry.blueprints import list_blueprints
from universal_ai_foundry.io import load_manifest
from universal_ai_foundry.planner import build_plan
from universal_ai_foundry.scaffold import scaffold_capsule
from universal_ai_foundry.security import review_manifest

app = typer.Typer(help="Universal AI Foundry command line tools.")
console = Console()


@app.command("list-blueprints")
def list_blueprint_command() -> None:
    table = Table("Name", "Modality", "Method", "Description")
    for blueprint in list_blueprints():
        table.add_row(
            blueprint.name,
            blueprint.modality.value,
            blueprint.method.value,
            blueprint.description,
        )
    console.print(table)


@app.command("init")
def init_capsule(
    target: Path,
    blueprint: str = typer.Option("llm-lora", "--blueprint", "-b"),
) -> None:
    manifest_path = scaffold_capsule(target, blueprint)
    console.print(f"Created AI Capsule at [bold]{manifest_path}[/bold]")


@app.command("validate")
def validate_capsule(path: Path) -> None:
    manifest = load_manifest(path)
    console.print_json(manifest.model_dump_json())


@app.command("plan")
def plan_capsule(path: Path) -> None:
    plan = build_plan(load_manifest(path))
    console.print_json(plan.model_dump_json())


@app.command("security-review")
def security_review(path: Path) -> None:
    manifest = load_manifest(path)
    findings = review_manifest(manifest, path.parent)
    console.print_json(json.dumps([finding.model_dump() for finding in findings]))
    if any(finding.severity in {"critical", "high"} for finding in findings):
        raise typer.Exit(code=2)


@app.command("serve")
def serve() -> None:
    import uvicorn

    uvicorn.run(fastapi_app, host="0.0.0.0", port=8010, reload=True)

