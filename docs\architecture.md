# Architecture

Universal AI Foundry is built around the AI Capsule abstraction.

## Core Concepts

## AI Capsule

An AI Capsule is a portable manifest and workspace convention for local generative AI training.

It defines:

- Modality
- Training method
- Dataset contract
- Base model
- Resource budget
- Safety policy
- Training commands
- Output locations

## Blueprint

A blueprint is a reusable starter manifest for a common training workflow. The first built-in blueprints are:

- `llm-lora`
- `image-diffusion-lora`
- `music-generator`
- `video-diffusion-lora`

## Planner

The planner converts a manifest into a human-readable execution plan. It intentionally does not execute training by default.

## Security Review

The security review checks for unsafe settings before a training job runs:

- Path traversal
- Workspace escape
- Remote code execution flags
- Missing dataset license
- Personal data indicators
- Risky shell command patterns
- Secret-like strings in commands
- Long-running or unusually large resource budgets

## API

The API exposes the same primitives used by the CLI:

- `GET /health`
- `GET /`
- `GET /v1/blueprints`
- `GET /v1/blueprints/{name}/manifest`
- `POST /v1/plan`
- `POST /v1/security-review`
- `POST /v1/run`

## GUI

The graphical interface is a local browser UI served by FastAPI. It intentionally does not require Node.js, Electron, or a cloud service, which keeps the project portable across Windows, Linux, and macOS.

## Future Runtime

The capsule layer is intentionally runtime-agnostic. Future runners can target local Python, Docker, Kubernetes jobs, Slurm, or managed GPU services while keeping the same manifest.
