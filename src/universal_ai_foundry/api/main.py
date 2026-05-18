from __future__ import annotations

from importlib.resources import files

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from universal_ai_foundry import __version__
from universal_ai_foundry.blueprints import get_blueprint, list_blueprints
from universal_ai_foundry.config import get_settings
from universal_ai_foundry.planner import build_plan
from universal_ai_foundry.runner import LocalRunner
from universal_ai_foundry.schemas import (
    BlueprintSummary,
    CapsuleManifest,
    ExecutionPlan,
    RunRequest,
    RunResult,
    SecurityFinding,
)
from universal_ai_foundry.security import review_manifest

app = FastAPI(
    title="Universal AI Foundry",
    version=__version__,
    description="Local AI Capsule orchestration API for generative AI training workflows.",
)

web_dir = files("universal_ai_foundry").joinpath("web")
app.mount("/static", StaticFiles(directory=str(web_dir)), name="static")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.get("/v1/blueprints", response_model=list[BlueprintSummary])
def blueprints() -> list[BlueprintSummary]:
    return list_blueprints()


@app.get("/", response_class=HTMLResponse)
def gui() -> str:
    return web_dir.joinpath("index.html").read_text(encoding="utf-8")


@app.get("/v1/blueprints/{name}/manifest", response_model=CapsuleManifest)
def blueprint_manifest(name: str) -> CapsuleManifest:
    return get_blueprint(name)


@app.post("/v1/plan", response_model=ExecutionPlan)
def plan(manifest: CapsuleManifest) -> ExecutionPlan:
    return build_plan(manifest)


@app.post("/v1/security-review", response_model=list[SecurityFinding])
def security_review(manifest: CapsuleManifest) -> list[SecurityFinding]:
    return review_manifest(manifest)


@app.post("/v1/run", response_model=RunResult)
def run_capsule(request: RunRequest) -> RunResult:
    runner = LocalRunner(get_settings().workspace)
    return runner.run(request.manifest, dry_run=request.dry_run)

