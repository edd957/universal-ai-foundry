# Universal AI Foundry

Open-source local training foundation for generative AI. Universal AI Foundry gives developers a portable "AI Capsule" format to scaffold, validate, plan, and run local experiments for LLMs, image generators, music generators, and video generators.

Built on May 18, 2026 with a modern Python stack and current generative AI ecosystem assumptions: PyTorch for local training, Hugging Face Transformers and PEFT for LLM adapters, Diffusers for image/video diffusion workflows, FastAPI for local orchestration, and Pydantic v2 for typed manifests.

## Why This Exists

Generative AI development is fragmented. Every modality has different scripts, folder structures, dependency stacks, GPU assumptions, dataset formats, and safety checks. Universal AI Foundry creates a shared base layer:

- One manifest format for generative AI projects.
- One local CLI to scaffold, validate, plan, and review training jobs.
- One API for local tools and dashboards.
- Built-in blueprints for LLM, image, music, and video training.
- Security review before executing training commands.
- Reproducible "AI Capsules" that behave like lightweight containers for AI projects.

## What Is An AI Capsule?

An AI Capsule is a portable project unit containing:

- `capsule.json` manifest
- dataset contract
- model target
- resource budget
- safety policy
- training command templates
- output artifact conventions

It is not a Docker replacement. It is a higher-level AI workflow contract that can run locally, inside Docker, or inside a future cluster runner.

## Capabilities

- Scaffold projects:
  - `llm-lora`
  - `image-diffusion-lora`
  - `music-generator`
  - `video-diffusion-lora`
- Validate manifests and dataset paths.
- Generate execution plans.
- Run security reviews for path traversal, secret leakage, unsafe remote-code flags, missing licenses, risky commands, and resource limits.
- Serve a local API for UI tools or automation.
- Keep heavy ML dependencies optional by modality.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uaf list-blueprints
uaf init my-local-llm --blueprint llm-lora
uaf validate my-local-llm/capsule.json
uaf plan my-local-llm/capsule.json
uaf security-review my-local-llm/capsule.json
```

## Local API

```bash
uaf serve
```

Open `http://localhost:8010` for the graphical AI Capsule Studio or `http://localhost:8010/docs` for the API.

## Graphical Interface

The GUI runs locally in the browser on Windows, Linux, and macOS. It lets users:

- choose a blueprint visually;
- edit capsule settings;
- preview the manifest;
- run a security review;
- generate a training plan.

## Repository Layout

```text
universal-ai-foundry/
|-- docs/
|-- examples/
|-- recipes/
|-- src/universal_ai_foundry/
|-- tests/
|-- Dockerfile
|-- docker-compose.yml
|-- Makefile
`-- pyproject.toml
```

## Safety First

Universal AI Foundry is designed for legitimate local model training and experimentation. It does not provide dataset scraping, model abuse workflows, malicious generation guidance, evasion tooling, or unsafe automation. Security review is a first-class command, not an afterthought.
