# Contributing

Thank you for reviewing Universal AI Foundry.

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Contribution Rules

- Keep blueprints safe and defensive.
- Do not add scraping or unauthorized data collection workflows.
- Do not add commands that require secrets in plain text.
- Add tests for manifest, planner, security, API, and scaffold behavior.
- Keep heavy training frameworks optional by modality.

