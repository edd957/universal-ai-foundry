.PHONY: test lint typecheck run-api list scaffold security clean

test:
	pytest

lint:
	ruff check .

typecheck:
	mypy src

run-api:
	uvicorn universal_ai_foundry.api.main:app --host 0.0.0.0 --port 8010 --reload

list:
	uaf list-blueprints

scaffold:
	uaf init demo-llm --blueprint llm-lora

security:
	uaf security-review examples/llm_lora_capsule.json

clean:
	python -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', '.ruff_cache', '.mypy_cache', 'htmlcov']]"

