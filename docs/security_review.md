# Security Review

Universal AI Foundry treats local training as a security-sensitive workflow.

## Reviewed Risks

- Dataset license ambiguity
- Personal data in training data
- Model remote-code execution
- Path traversal in dataset or output paths
- Secret-like tokens in command templates
- Risky shell patterns
- Excessive resource consumption
- Missing human review before execution

## Default Policy

The default capsule policy blocks remote code, requires dataset license review, blocks secret patterns, disables network downloads, and requires human review before execution.

## Recommended Local Workflow

1. Scaffold a capsule.
2. Edit dataset and model details.
3. Run `uaf validate`.
4. Run `uaf plan`.
5. Run `uaf security-review`.
6. Review findings.
7. Run modality-specific training scripts only after approval.

The local API runner defaults to `dry_run=true`. Non-dry execution is blocked when critical or high findings are present.

## Non-Goals

The project does not provide scraping, unauthorized data collection, prompt abuse automation, malware generation, credential theft, or unsafe deployment automation.
