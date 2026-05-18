from fastapi.testclient import TestClient

from universal_ai_foundry.api.main import app
from universal_ai_foundry.blueprints import get_blueprint


def test_health() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_gui_index() -> None:
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert "AI Capsule Studio" in response.text


def test_plan_endpoint() -> None:
    client = TestClient(app)
    manifest = get_blueprint("video-diffusion-lora")

    response = client.post("/v1/plan", json=manifest.model_dump(mode="json"))

    assert response.status_code == 200
    assert response.json()["modality"] == "video"


def test_run_endpoint_defaults_to_dry_run() -> None:
    client = TestClient(app)
    manifest = get_blueprint("llm-lora")
    manifest.dataset.license = "cc-by-4.0"

    response = client.post(
        "/v1/run",
        json={"manifest": manifest.model_dump(mode="json"), "dry_run": True},
    )

    assert response.status_code == 200
    assert response.json()["dry_run"] is True
